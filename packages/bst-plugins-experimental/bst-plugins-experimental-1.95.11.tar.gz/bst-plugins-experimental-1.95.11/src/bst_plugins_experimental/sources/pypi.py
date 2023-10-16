#
#  Copyright (C) 2020 Codethink Limited
#  Copyright (C) 2020-2022 Seppo Yli-Olli
#  Copyright (C) 2021 Abderrahim Kitouni
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2 of the License, or (at your option) any later version.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	 See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library. If not, see <http://www.gnu.org/licenses/>.
#
#  Authors:
#         Valentin David <valentin.david@codethink.co.uk>
#         Seppo Yli-Olli <seppo.yli-olli@iki.fi>
#         Abderrahim Kitouni <akitouni@gnome.org>

import contextlib
import os
import re
import fnmatch
import shutil
import tarfile
import zipfile
import stat
import urllib.request
import json

from buildstream import Source, SourceError, SourceFetcher, utils
import packaging.utils


def strip_top_dir(members, attr):
    for member in members:
        path = getattr(member, attr)
        trail_slash = path.endswith("/")
        path = path.rstrip("/")
        splitted = getattr(member, attr).split("/", 1)
        if len(splitted) == 2:
            new_path = splitted[1]
            if trail_slash:
                new_path += "/"
            setattr(member, attr, new_path)
            yield member


# We do not support parsing HTML
ACCEPT = "application/vnd.pypi.simple.v1+json"


class Downloader(SourceFetcher):
    def __init__(self, source, url, name):
        super().__init__()
        self.mark_download_url(url)
        self.suffix = None
        self.sha256sum = None
        self.source = source
        self.url = url
        self.mirror_directory = os.path.join(
            self.source.get_mirror_directory(), utils.url_directory_name(name)
        )

    @property
    def mirror_file(self):
        return os.path.join(self.mirror_directory, self.sha256sum)

    def fetch(self, alias_override=None):
        baseurl = self.source.translate_url(
            self.url, alias_override=alias_override
        )
        url = baseurl + self.suffix
        # Loosely based on _downloadablefilesource.py

        with contextlib.ExitStack() as stack:
            stack.enter_context(
                self.source.timed_activity("Fetching from {}".format(url))
            )
            try:
                tempdir = stack.enter_context(self.source.tempdir())
                default_name = os.path.basename(url)
                request = urllib.request.Request(url)
                request.add_header("Accept", "*/*")
                request.add_header("User-Agent", "BuildStream/2")

                response = stack.enter_context(urllib.request.urlopen(request))
                info = response.info()
                filename = info.get_filename(default_name)
                filename = os.path.basename(filename)
                local_file = os.path.join(tempdir, filename)

                with open(local_file, "wb") as dest:
                    shutil.copyfileobj(response, dest)
                response.close()

                os.makedirs(self.mirror_directory, exist_ok=True)

                sha256 = self.sha256sum
                computed = utils.sha256sum(local_file)
                if sha256 != computed:
                    raise SourceError(
                        f"{url} expected hash {sha256}, got {computed}"
                    )
                os.rename(local_file, self.mirror_file)
                return sha256

            except (
                urllib.error.URLError,
                urllib.error.ContentTooShortError,
                OSError,
            ) as e:
                raise SourceError(
                    f"{self}: Error mirroring {url}: {e}", temporary=True
                ) from e

    def set_ref(self, suffix, sha256sum):
        self.suffix = suffix
        self.sha256sum = sha256sum


def filter_files(files, matcher):
    processed = {}
    for file in files:
        if file["yanked"]:
            continue
        try:
            _, version = packaging.utils.parse_sdist_filename(file["filename"])
        except (
            packaging.utils.InvalidSdistFilename,
            packaging.utils.InvalidVersion,
        ):
            continue
        if matcher.should_include(version) and not matcher.should_exclude(
            version
        ):
            processed[version] = file
    return processed


class Matcher:
    def __init__(self, prereleases, include, exclude):
        self.prereleases = prereleases
        self.include = [
            re.compile(fnmatch.translate(item)) for item in include
        ]
        self.exclude = [
            re.compile(fnmatch.translate(item)) for item in exclude
        ]

    def should_include(self, version):
        if not self.prereleases and version.is_prerelease:
            return False
        for matcher in self.include:
            if not matcher.match(str(version)):
                return False
        return True

    def should_exclude(self, version):
        for matcher in self.exclude:
            if matcher.match(str(version)):
                return True
        return False


class PyPISource(Source):
    BST_MIN_VERSION = "2.0"

    REST_API = "https://pypi.org/simple/{name}"
    STORAGE_ROOT = "https://files.pythonhosted.org/packages/"
    KEYS = [
        "url",
        "name",
        "ref",
        "prereleases",
        "include",
        "exclude",
    ] + Source.COMMON_CONFIG_KEYS

    def configure(self, node):
        node.validate_keys(self.KEYS)

        self.name = node.get_str("name")

        self.matcher = Matcher(
            node.get_bool("prereleases", False),
            node.get_str_list("include", []),
            node.get_str_list("exclude", []),
        )

        self.original_url = node.get_str("url", self.STORAGE_ROOT)

        self.mark_download_url(self.original_url)
        self.fetcher = Downloader(self, self.original_url, self.name)
        self.load_ref(node)

    @property
    def url(self):
        return self.translate_url(self.original_url)

    def preflight(self):
        pass

    def get_unique_key(self):
        return [self.fetcher.suffix, self.fetcher.sha256sum]

    def load_ref(self, node):
        ref_mapping = node.get_mapping("ref", None)
        if ref_mapping:
            self.fetcher.set_ref(
                ref_mapping.get_str("suffix"),
                ref_mapping.get_str("sha256sum"),
            )

    def get_ref(self):
        if self.fetcher.suffix and self.fetcher.sha256sum:
            return {
                "sha256sum": self.fetcher.sha256sum,
                "suffix": self.fetcher.suffix,
            }
        return None

    def set_ref(self, ref, node):
        self.fetcher.set_ref(ref["suffix"], ref["sha256sum"])
        node["ref"] = ref

    def track(self):
        request = urllib.request.Request(
            self.REST_API.format(name=self.name), headers={"ACCEPT": ACCEPT}
        )
        with urllib.request.urlopen(request) as response:
            payload = json.loads(response.read())

        if not payload["files"]:
            raise SourceError(
                f"{self}: Cannot find any tracking for {self.name}"
            )
        files = filter_files(payload["files"], self.matcher)
        if not files:
            self.warn("{self}: No matching release found")
            return None

        latest = files[max(files)]
        return {
            "sha256sum": latest["hashes"]["sha256"],
            "suffix": latest["url"].replace(self.STORAGE_ROOT, ""),
        }

    def stage(self, directory):
        if not os.path.exists(self.fetcher.mirror_file):
            raise SourceError(
                f"{self}: Cannot find mirror file {self.fetcher.mirror_file}"
            )
        if self.url.endswith(".zip"):
            with zipfile.ZipFile(self.fetcher.mirror_file, mode="r") as zipf:
                exec_rights = (stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO) & ~(
                    stat.S_IWGRP | stat.S_IWOTH
                )
                noexec_rights = exec_rights & ~(
                    stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
                )
                # Taken from zip plugin. It is needed to ensure reproducibility of permissions
                for member in strip_top_dir(zipf.infolist(), "filename"):
                    written = zipf.extract(member, path=directory)
                    rel = os.path.relpath(written, start=directory)
                    assert not os.path.isabs(rel)
                    rel = os.path.dirname(rel)
                    while rel:
                        os.chmod(os.path.join(directory, rel), exec_rights)
                        rel = os.path.dirname(rel)

                    if os.path.islink(written):
                        pass
                    elif os.path.isdir(written):
                        os.chmod(written, exec_rights)
                    else:
                        os.chmod(written, noexec_rights)
        else:
            with tarfile.open(self.fetcher.mirror_file, "r:gz") as tar:
                tar.extractall(
                    path=directory,
                    members=strip_top_dir(tar.getmembers(), "path"),
                )

    def is_cached(self):
        return os.path.isfile(self.fetcher.mirror_file)

    def get_source_fetchers(self):
        return [self.fetcher]


def setup():
    return PyPISource
