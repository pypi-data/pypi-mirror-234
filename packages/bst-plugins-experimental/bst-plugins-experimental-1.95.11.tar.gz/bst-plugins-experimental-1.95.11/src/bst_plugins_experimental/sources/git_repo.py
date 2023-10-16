"""
git_repo - plugin for git repo handling
==============================================

**Usage:**

.. code:: yaml

   # Specify the git_repo source kind
   kind: git_repo

   # Specify the repository url, using an alias defined
   # in your project configuration is recommended.
   url: upstream:repo.git

   # Optionally specify a tracking branch or tag, this
   # will be used to update the 'ref' when refreshing the pipeline.
   # Tracking supports globs that can be used to filter wanted
   # tag from repository.
   track: release-*

   # Specify the commit checksum, this must be specified in order
   # to checkout sources and build, but can be automatically
   # updated if the 'track' attribute was specified.
   ref: release-3.0-0-gcad743283c43c776d03ae05578f353f728be62e3

   # Specify tracks to exclude in case there's eg bad tags by upstream
   exclude:
   - release-3.0.1

   # Declare the format of ref after tracking. When tracking branches,
   # fetching will be required if sha1 is not used. If git-describe is
   # given, ref follows output of `git describe`. Regardless of format,
   # `git describe` and `git log -1` are expected to work in the sandbox.
   ref-format: git-describe
"""

import fnmatch
import re
import os
import threading
import netrc

from enum import Enum
from stat import S_ISDIR, S_ISLNK
from dataclasses import dataclass
from urllib.parse import urlparse

from buildstream import Source, SourceFetcher, SourceError
from buildstream.utils import url_directory_name

from dulwich.repo import Repo
from dulwich.objects import Commit, Tag, S_ISGITLINK
from dulwich.client import get_transport_and_path, HTTPUnauthorized
from dulwich.errors import GitProtocolError, NotGitRepository
from dulwich.refs import ANNOTATED_TAG_SUFFIX


REF_REGEX = re.compile(r"(?:(.*)(?:-(\d+)-g))?([0-9a-f]{40})")
SPLITTER_REGEX = re.compile(rb"[a-zA-Z]+|[0-9]+")


def pattern_to_regex(pattern):
    """
    Transforms a glob pattern into a regex to match refs.

    If the pattern doesn't start with "refs/", it will be considered to only match refs in
    refs/tags/ and refs/heads.
    """
    if pattern.startswith("refs/"):
        return re.compile(fnmatch.translate(pattern).encode())

    return re.compile(
        ("refs/(heads|tags)/" + fnmatch.translate(pattern)).encode()
    )


def version_sort_key(elt):
    """
    A sort key that can be used to versions. It sorts letters before numbers (so 1.beta is earlier
    than 1.0) and disregards separators (so 1.beta, 1~beta and 1beta are the same).
    """
    return [
        # to sort letters before digits
        (-1, part) if part.isalpha() else (int(part), "")
        for part in SPLITTER_REGEX.findall(elt)
    ]


def get_matching_refs(refs, tracking, exclude):
    real_refs = {ref for ref in refs if not ref.endswith(b"^{}")}
    matching_regex = pattern_to_regex(tracking)

    matching_refs = [ref for ref in real_refs if matching_regex.match(ref)]

    if exclude:
        exclude_regexs = [pattern_to_regex(pattern) for pattern in exclude]
        matching_refs = [
            ref
            for ref in matching_refs
            if not any(regex.match(ref) for regex in exclude_regexs)
        ]

    return matching_refs


def get_netrc_credentials(url):
    p = urlparse(url)
    if p.scheme != "https":
        return {}
    try:
        n = netrc.netrc()
        creds = n.authenticators(p.hostname)

        if creds is not None:
            # creds is a tuple (username, account, password)
            return {"username": creds[0], "password": creds[2]}
    except FileNotFoundError:
        pass

    return {}


def init_repo(mirror_dir):
    """
    Open a repo at the given mirror_dir, creating an empty bare repo if it doesn't exist.
    """
    try:
        return Repo.init_bare(mirror_dir, mkdir=True)
    except FileExistsError:
        return Repo(mirror_dir, bare=True)


def collect_objects(mirror, commit, base, trees_only):
    if commit == base:
        commits = {commit}
    elif base is None:
        commits = {entry.commit for entry in mirror.get_walker(commit.id)}
    else:
        commits = {
            entry.commit
            for entry in mirror.get_walker(commit.id, base.parents)
        }

    # All the tree objects. `git log .` and `git describe --dirty` need them
    trees = set(commit.tree for commit in commits)
    objects = set()

    while trees:
        tree = trees.pop()

        if tree in objects:
            continue
        objects.add(tree)

        for _, mode, sha in mirror[tree].items():
            if S_ISDIR(mode):
                trees.add(sha)
            elif S_ISLNK(mode) or (not trees_only and not S_ISGITLINK(mode)):
                objects.add(sha)

    objects = {mirror[sha] for sha in objects}

    return commits | objects


def stage_repository(mirror, directory, objects, refs, remotes, pack=False):
    object_ids = {obj.id for obj in objects}
    shallow = {
        obj.id
        for obj in objects
        if isinstance(obj, Commit) and not object_ids.issuperset(obj.parents)
    }

    with Repo.init(directory) as dest:
        if pack:
            dest.object_store.add_objects([(obj, None) for obj in objects])
        else:
            for obj in objects:
                dest.object_store.add_object(obj)

        for ref, target in refs.items():
            dest.refs[ref] = target

        dest.update_shallow(shallow, [])

        conf = dest.get_config()
        for remote, url in remotes.items():
            conf.set(("remote", remote), "url", url)
        conf.write_to_path()

    # checkout
    with Repo(directory, object_store=mirror.object_store) as dest:
        dest.reset_index()


def git_describe(repo, revision):
    """
    Returns the equivalent of `git describe --tags --abbrev=40`
    """
    # Get a list of all tags
    tags = repo.refs.as_dict(b"refs/tags")

    if not tags:
        return revision

    commit_tags = {}
    for tag_name, tag_sha in list(tags.items()):
        commit = repo.get_object(tag_sha)
        while isinstance(commit, Tag):
            commit = repo.get_object(commit.object[1])

        commit_tags[commit.id] = tag_name.decode()

    count = 0

    walker = repo.get_walker([revision.encode()])
    for entry in walker:
        commit_id = entry.commit.id
        if commit_id in commit_tags:
            return f"{commit_tags[commit_id]}-{count}-g{revision}"

        count += 1

    return revision


LOCKS = {}


class GitMirror(SourceFetcher):
    def __init__(self, source, url, ref):
        super().__init__()
        self.mark_download_url(url)

        self.source = source
        self.url = url

        tag, depth, sha = REF_REGEX.match(ref).groups()

        self.sha = sha
        self.tagref = f"refs/tags/{tag}".encode() if tag else None
        self.depth = int(depth) + 1 if depth else None

    def fetch(self, alias_override=None):
        url = self.source.translate_url(
            self.url, alias_override=alias_override
        )
        lock = LOCKS.setdefault(self.source.mirror_dir, threading.Lock())

        with lock, init_repo(
            self.source.mirror_dir
        ) as repo, self.source.timed_activity(f"Fetching from {url}"):
            if self.sha.encode() in repo and (
                not self.tagref or self.tagref in repo.refs
            ):
                return

            self.source.status(f"Fetching {self.sha}")

            # Git protocol version 2 allows requesting any object, not necessarily an object
            # pointed to by a ref. Unfortunately, dulwich doesn't support protocol version 2.
            # In practice a lot of version 2 servers accept this even when speaking protocol
            # version 1. We try to take advantage of this by requesting exact refs.
            def exact_want(refs, depth=None):
                wanted = set([self.sha.encode()])
                if not self.tagref:
                    return wanted

                if self.tagref in refs:
                    wanted.add(refs[self.tagref])
                    return wanted

                raise SourceError(
                    f"ref {self.tagref.decode()} not found in remote {url}"
                )

            # Another optimisation we can do is to request all the refs that match what we're
            # tracking. This is almost guaranteed to get us what we need without downloading
            # everything.
            def track_want(refs, depth=None):
                wanted_refs = get_matching_refs(
                    refs, self.source.tracking, self.source.exclude
                )

                if self.tagref:
                    wanted_refs.append(self.tagref)

                self.source.status(
                    "fetching tracked refs",
                    detail=b"\n".join(wanted_refs).decode(),
                )
                wanted = {refs[ref] for ref in wanted_refs}
                return wanted

            credentials = get_netrc_credentials(url)
            client, path = get_transport_and_path(url, **credentials)

            try:
                try:
                    remote_refs = client.fetch(
                        path,
                        repo,
                        determine_wants=exact_want,
                        depth=self.depth,
                    )
                except GitProtocolError as e:
                    if "not our ref" not in str(e):
                        raise

                    remote_refs = client.fetch(
                        path,
                        repo,
                        determine_wants=track_want,
                        depth=self.depth,
                    )

                    # Fall back to downloading everything
                    if self.sha.encode() not in repo:
                        remote_refs = client.fetch(
                            path, repo, depth=self.depth
                        )
            except (GitProtocolError, HTTPUnauthorized, NotGitRepository) as e:
                raise SourceError(f"failed to fetch: {e}") from e
            except NotImplementedError as e:
                self.source.warn(f"not implemented {e}")
                if client.dumb:
                    raise SourceError(
                        "Fetching from a dumb repository is not currently supported, "
                        "please set up a mirror on a smart server"
                    ) from e
                raise SourceError(f"failed to fetch: {e}") from e

            # check that we actually pulled the required commit
            if self.sha.encode() not in repo:
                raise SourceError(f"{self.sha} not found in remote {url}")

            if self.tagref:
                repo.refs.add_if_new(self.tagref, remote_refs[self.tagref])
                return

            local_refs = repo.get_refs()

            extra_wants = []
            extra_haves = []
            for ref in remote_refs:
                if not ref.startswith(b"refs/tags"):
                    continue
                if ref.endswith(ANNOTATED_TAG_SUFFIX):
                    continue
                if ref in local_refs:
                    continue
                if remote_refs[ref] in repo:
                    repo.refs.add_if_new(ref, remote_refs[ref])
                else:
                    peeled_ref = ref + ANNOTATED_TAG_SUFFIX
                    if (
                        peeled_ref in remote_refs
                        and remote_refs[peeled_ref] in repo
                    ):
                        extra_haves.append(remote_refs[peeled_ref])
                        extra_wants.append(remote_refs[ref])

            if extra_wants:
                self.source.status(f"Fetching {len(extra_wants)} extra tags")
                f, commit, abort = repo.object_store.add_pack()
                try:
                    walker = repo.get_graph_walker(extra_haves)
                    remote_refs = client.fetch_pack(
                        path, lambda _: extra_wants, walker, f.write
                    )
                except Exception as e:
                    # should be more specific
                    abort()
                    raise SourceError(f"failed to fetch: {e}") from e

                commit()
                for ref, value in remote_refs.items():
                    if value in extra_wants:
                        repo.refs.add_if_new(ref, value)


class RefFormat(Enum):
    SHA1 = "sha1"
    GIT_DESCRIBE = "git-describe"


@dataclass
class RepoInfo:
    primary: bool
    ref: str
    url: str


class GitSource(Source):
    BST_MIN_VERSION = "2.0"

    def configure(self, node):
        CONFIG_KEYS = ["ref", "url", "track", "exclude", "ref-format"]

        node.validate_keys(Source.COMMON_CONFIG_KEYS + CONFIG_KEYS)
        self.ref = None
        self.load_ref(node)

        self.url = node.get_str("url")
        self.mark_download_url(self.url)

        if self.url.endswith(".git"):
            norm_url = self.url[:-4]
        else:
            norm_url = self.url

        self.mirror_dir = os.path.join(
            self.get_mirror_directory(),
            url_directory_name(norm_url) + ".git",
        )

        self.tracking = node.get_str("track", None)
        self.exclude = node.get_str_list("exclude", [])

        self.ref_format = node.get_enum(
            "ref-format", RefFormat, RefFormat.SHA1
        )

        # make the url-manifest script happy
        self.mirror = RepoInfo(primary=True, ref=self.ref, url=self.url)

    def preflight(self):
        pass

    def get_unique_key(self):
        return {"ref": self.ref, "bugfix": 1}

    # loading and saving refs
    def load_ref(self, node):
        if "ref" not in node:
            return
        ref = node.get_str("ref")
        if REF_REGEX.match(ref) is None:
            raise SourceError(f"ref {ref} is not in the expected format")
        self.ref = ref

    def get_ref(self):
        return self.ref

    def set_ref(self, ref, node):
        self.ref = ref
        node["ref"] = ref

    def is_cached(self):
        tag, _, sha = REF_REGEX.match(self.ref).groups()

        with Repo(self.mirror_dir, bare=True) as repo:
            cached = sha.encode() in repo
            if tag:
                ref = b"refs/tags/" + tag.encode()
                cached_ref = ref in repo

                cached = cached and cached_ref

        return cached

    def track(self):
        if not self.tracking:
            return None

        url = self.translate_url(self.url)
        self.status(f"Tracking {self.tracking} from {url}")

        credentials = get_netrc_credentials(url)
        client, path = get_transport_and_path(url, **credentials)

        try:
            refs = client.get_refs(path)
        except (GitProtocolError, HTTPUnauthorized) as exc:
            raise SourceError(f"Failed to track {url}") from exc

        matching_refs = get_matching_refs(refs, self.tracking, self.exclude)
        if not matching_refs:
            raise SourceError("No matching refs")

        self.debug(
            "Refs to be tracked", detail=b"\n".join(matching_refs).decode()
        )

        ref = max(matching_refs, key=version_sort_key)

        # peel the ref if possible
        peeled_ref = ref + b"^{}"
        if peeled_ref in refs:
            resolved = refs[peeled_ref]
        else:
            resolved = refs[ref]

        # Use str instead of bytes from here on
        ref = ref.decode()
        resolved = resolved.decode()

        self.status(f"Tracked {ref}: {resolved}")

        if self.ref_format == RefFormat.SHA1:
            return resolved

        if "tags" in ref:
            tag = ref.split("/", 2)[-1]
            return f"{tag}-0-g{resolved}"

        # Need to fetch to generate the ref in git-describe format
        fetcher = GitMirror(self, self.url, resolved)
        fetcher.fetch()

        with Repo(self.mirror_dir) as repo:
            return git_describe(repo, resolved)

    def get_source_fetchers(self):
        yield GitMirror(self, self.url, self.ref)

    def stage(self, directory):
        tag, _, sha = REF_REGEX.match(self.ref).groups()
        self.status(f"Checking out {sha}")

        with Repo(self.mirror_dir, bare=True) as mirror:
            refs = {b"HEAD": sha.encode()}
            tag_objects = set()

            commit = mirror[sha.encode()]
            base = mirror[sha.encode()]

            if tag:
                tag_ref = f"refs/tags/{tag}".encode()
                tag_target = mirror[tag_ref]
                refs[tag_ref] = tag_target.id

                if isinstance(tag_target, Tag):
                    # Annotated tag
                    tag_objects.add(tag_target)
                    tag_target = mirror[tag_target.object[1]]

                assert isinstance(
                    tag_target, Commit
                ), f"Tag {tag} does not point to a commit (type {type(tag_target)}"

                base = tag_target

            objects = collect_objects(mirror, commit, base, True)
            self.status(f"Adding {len(objects)} objects")

            # `|` means union
            stage_repository(
                mirror, directory, tag_objects | objects, refs, {}, pack=False
            )

    def init_workspace(self, directory):
        tag, _, sha = REF_REGEX.match(self.ref).groups()
        self.status(f"Checking out {sha}")

        with Repo(self.mirror_dir, bare=True) as mirror:
            refs = {b"HEAD": sha.encode()}
            remotes = {"origin": self.translate_url(self.url)}

            commit = mirror[sha.encode()]
            objects = collect_objects(mirror, commit, None, False)

            tag_objects = set()

            for tag, tag_sha in mirror.refs.as_dict(b"refs/tags").items():
                tag_ref = b"refs/tags/" + tag
                tag_target = mirror[tag_sha]
                tag_obj = None

                if isinstance(tag_target, Commit):
                    if tag_target in objects:
                        refs[tag_ref] = tag_target.id

                    continue

                # Annotated tag
                tag_obj = tag_target
                tag_target = mirror[tag_target.object[1]]

                assert isinstance(
                    tag_target, Commit
                ), f"Tag {tag} does not point to a commit (type {type(tag_target)}"

                if tag_target in objects:
                    tag_objects.add(tag_obj)
                    refs[tag_ref] = tag_obj.id

            self.status(f"Adding {len(objects)} objects")

            # `|` means union
            stage_repository(
                mirror,
                directory,
                tag_objects | objects,
                refs,
                remotes,
                pack=True,
            )


def setup():
    return GitSource
