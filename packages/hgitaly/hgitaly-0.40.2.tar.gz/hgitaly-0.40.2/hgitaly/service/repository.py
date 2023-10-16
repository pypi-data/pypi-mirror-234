# Copyright 2020 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
import gc
from grpc import StatusCode
from io import BytesIO
import itertools
import logging
import os
from pathlib import Path
from collections import deque
import re
import shutil
import tempfile

from mercurial import (
    archival,
    pycompat,
    scmutil,
    hg,
    node,
)
from mercurial.commands import (
    bundle,
)

from heptapod.gitlab.branch import gitlab_branch_from_ref
from hgext3rd.heptapod import (
    backup_additional,
    restore_additional,
)
from hgext3rd.heptapod.branch import set_default_gitlab_branch
from hgext3rd.heptapod.special_ref import write_gitlab_special_ref
from hgext3rd.heptapod.keep_around import (
    create_keep_around,
    parse_keep_around_ref,
)

from .. import (
    manifest,
    message,
)
from ..branch import (
    iter_gitlab_branches,
)
from ..errors import (
    ServiceError,
    not_implemented,
)
from ..gitlab_ref import (
    parse_special_ref,
    ensure_special_refs,
)
from ..logging import LoggerAdapter
from ..path import (
    InvalidPath,
    validate_relative_path,
)
from ..repository import (
    get_gitlab_project_full_path,
    set_gitlab_project_full_path,
    unbundle,
)
from ..revision import (
    ALL_CHANGESETS,
    CHANGESET_HASH_BYTES_REGEXP,
    gitlab_revision_changeset,
    resolve_revspecs_positive_negative,
)
from ..servicer import HGitalyServicer
from ..stream import (
    WRITE_BUFFER_SIZE,
    streaming_request_tempfile_extract,
)
from ..util import (
    chunked,
)
from ..stub.repository_pb2 import (
    BackupCustomHooksRequest,
    BackupCustomHooksResponse,
    CreateBundleRequest,
    CreateBundleResponse,
    CreateBundleFromRefListRequest,
    CreateBundleFromRefListResponse,
    CreateRepositoryRequest,
    CreateRepositoryResponse,
    CreateRepositoryFromBundleRequest,
    CreateRepositoryFromBundleResponse,
    FetchBundleRequest,
    FetchBundleResponse,
    FindMergeBaseRequest,
    FindMergeBaseResponse,
    FullPathRequest,
    FullPathResponse,
    GetRawChangesRequest,
    GetRawChangesResponse,
    GetCustomHooksRequest,
    GetCustomHooksResponse,
    RepositoryExistsRequest,
    RepositoryExistsResponse,
    GetArchiveRequest,
    GetArchiveResponse,
    HasLocalBranchesRequest,
    HasLocalBranchesResponse,
    RemoveAllRequest,
    RemoveAllResponse,
    RemoveRepositoryRequest,
    RemoveRepositoryResponse,
    RestoreCustomHooksRequest,
    RestoreCustomHooksResponse,
    SearchFilesByContentRequest,
    SearchFilesByContentResponse,
    SearchFilesByNameRequest,
    SearchFilesByNameResponse,
    SetCustomHooksRequest,
    SetCustomHooksResponse,
    SetFullPathRequest,
    SetFullPathResponse,
    WriteRefRequest,
    WriteRefResponse,
    ApplyGitattributesRequest,
    ApplyGitattributesResponse,
)
from ..stub.repository_pb2_grpc import RepositoryServiceServicer
from ..stub.shared_pb2 import (
    Repository,
)


base_logger = logging.getLogger(__name__)
DEFAULT_BRANCH_FILE_NAME = b'default_gitlab_branch'
ARCHIVE_FORMATS = {
    GetArchiveRequest.Format.Value('ZIP'): b'zip',
    GetArchiveRequest.Format.Value('TAR'): b'tar',
    GetArchiveRequest.Format.Value('TAR_GZ'): b'tgz',
    GetArchiveRequest.Format.Value('TAR_BZ2'): b'tbz2',
}
SEARCH_FILES_FILTER_MAX_LENGTH = 1000
"""Maximum size of regular expression in SearchFiles methods.

Value taken from Gitaly's `internal/gitaly/service/repository/search_files.go'
"""


class RepositoryCreationError(ServiceError):
    """Specific exception for creation problems."""


class RepositoryServicer(RepositoryServiceServicer, HGitalyServicer):
    """RepositoryServiceService implementation.
    """

    STATUS_CODE_STORAGE_NOT_FOUND = StatusCode.INVALID_ARGUMENT

    def FindMergeBase(self,
                      request: FindMergeBaseRequest,
                      context) -> FindMergeBaseResponse:
        repo = self.load_repo(request.repository, context)
        if len(request.revisions) < 2:
            context.abort(StatusCode.INVALID_ARGUMENT,
                          'at least 2 revisions are required')

        ctxs = []
        for rev in request.revisions:
            ctx = gitlab_revision_changeset(repo, rev)
            if ctx is None:
                return FindMergeBaseResponse()
            ctxs.append(ctx)

        # Some of the changesets may be obsolete (if addressed by SHAs).
        # The GCA may be obsolete as well (meaning that one of ctxs is
        # also obsolete). TODO add test for obsolete cases
        repo = repo.unfiltered()
        gca = repo.revs(b"ancestor(%ld)", ctxs).first()
        base = repo[gca].hex() if gca is not None else ''
        return FindMergeBaseResponse(base=base)

    def RepositoryExists(self,
                         request: RepositoryExistsRequest,
                         context) -> RepositoryExistsResponse:
        try:
            self.load_repo_inner(request.repository, context)
            exists = True
        except KeyError as exc:
            if exc.args[0] == 'storage':
                context.abort(
                    StatusCode.INVALID_ARGUMENT,
                    f'GetStorageByName: no such storage: "{exc.args[1]}"'
                )
            exists = False
        except ValueError as exc:
            context.abort(StatusCode.INVALID_ARGUMENT, exc.args[0])

        return RepositoryExistsResponse(exists=exists)

    def GetArchive(self,
                   request: GetArchiveRequest,
                   context) -> GetArchiveResponse:
        repo = self.load_repo(request.repository, context)
        ctx = repo[request.commit_id]

        patterns = []
        path = request.path
        if path:
            try:
                path = validate_relative_path(repo, path)
            except InvalidPath:
                context.abort(StatusCode.INVALID_ARGUMENT,
                              "Invalid path: '%s'" % path)

            patterns.append(b"path:" + path)

        match = scmutil.match(ctx, pats=patterns, opts={})

        # using an anonymous (not linked) temporary file
        # TODO OPTIM check if archive is not by any chance
        # using a tempfile already…
        with tempfile.TemporaryFile(
                mode='wb+',  # the default, but let's insist on binary here
                buffering=WRITE_BUFFER_SIZE) as tmpf:
            try:
                archival.archive(
                    repo,
                    tmpf,
                    ctx.node(),
                    ARCHIVE_FORMATS[request.format],
                    # TODO this is the default but check what it means:
                    True,  # decode
                    match,
                    request.prefix.encode(),
                    subrepos=False  # maybe later, check GitLab's standard
                )
            finally:
                gc.collect()

            tmpf.seek(0)
            while True:
                data = tmpf.read(WRITE_BUFFER_SIZE)
                if not data:
                    break
                yield GetArchiveResponse(data=data)

    def HasLocalBranches(self,
                         request: HasLocalBranchesRequest,
                         context) -> HasLocalBranchesResponse:
        repo = self.load_repo(request.repository, context)
        # the iteration should stop as soon at first branchmap entry which
        # has a non closed head (but all heads in that entry would be checked
        # to be non closed)
        return HasLocalBranchesResponse(value=any(iter_gitlab_branches(repo)))

    def WriteRef(
            self,
            request: WriteRefRequest,
            context) -> WriteRefResponse:
        """Create or update a GitLab ref.

        The reference Gitaly implementation treats two cases, ``HEAD`` being
        the only supported symbolic ref. Excerpt as of GitLab 13.9.0::

          func (s *server) writeRef(ctx context.Context,
                                    req *gitalypb.WriteRefRequest) error {
            if string(req.Ref) == "HEAD" {
              return s.updateSymbolicRef(ctx, req)
            }
            return updateRef(ctx, s.cfg, s.gitCmdFactory, req)
          }

        On the other hand, the target revision is fully resolved, even
        when setting a non-symbolic ref.
        """
        logger = LoggerAdapter(base_logger, context)
        ref, target = request.ref, request.revision
        repo = self.load_repo(request.repository, context)

        try:
            special_ref_name = parse_special_ref(ref)
            if special_ref_name is not None:
                target_sha = gitlab_revision_changeset(repo, target)
                ensure_special_refs(repo)
                write_gitlab_special_ref(repo, special_ref_name, target_sha)
                return WriteRefResponse()

            keep_around = parse_keep_around_ref(ref)
            if keep_around is not None:
                if (CHANGESET_HASH_BYTES_REGEXP.match(keep_around) is None
                        or target != keep_around):
                    context.abort(
                        StatusCode.INVALID_ARGUMENT,
                        "Invalid target %r for keep-around %r. Only full "
                        "changeset ids in hexadecimal form are accepted and "
                        "target must "
                        "match the ref name" % (target, ref)
                    )

                create_keep_around(repo, target)
                return WriteRefResponse()
        except Exception:
            logger.exception(
                "WriteRef failed for Repository %r on storage %r",
                request.repository.relative_path,
                request.repository.storage_name)
            return WriteRefResponse()

        if ref != b'HEAD':
            context.abort(
                StatusCode.INVALID_ARGUMENT,
                "Setting ref %r is not implemented in Mercurial (target %r) "
                "Does not make sense in the case of branches and tags, "
                "except maybe for bookmarks." % (ref, target))

        target_branch = gitlab_branch_from_ref(target)
        if target_branch is None:
            context.abort(StatusCode.INVALID_ARGUMENT,
                          "The default GitLab branch can only be set "
                          "to a branch ref, got %r" % target)

        set_default_gitlab_branch(repo, target_branch)
        return WriteRefResponse()

    def ApplyGitattributes(self, request: ApplyGitattributesRequest,
                           context) -> ApplyGitattributesResponse:
        """Method used as testing bed for the `not_implemented` helper.

        It is unlikely we ever implement this one, and if we do something
        similar, we'll probably end up defining a ApplyHgAttributes anyway.
        """
        not_implemented(context, issue=1234567)

    def CreateRepository(self, request: CreateRepositoryRequest,
                         context) -> CreateRepositoryResponse:
        try:
            self.hg_init_repository(request.repository, context)
        finally:
            # response is the same in case of error or success
            return CreateRepositoryResponse()

    def GetRawChanges(self, request: GetRawChangesRequest,
                      context) -> GetRawChangesResponse:
        not_implemented(context, issue=79)  # pragma no cover

    def SearchFilesByName(self, request: SearchFilesByNameRequest,
                          context) -> SearchFilesByNameResponse:
        repo = self.load_repo(request.repository, context)
        changeset = gitlab_revision_changeset(repo, request.ref)
        if changeset is None:
            yield SearchFilesByNameResponse()
            return

        query = request.query
        if not query:
            context.abort(StatusCode.INVALID_ARGUMENT, "no query given")

        subdir = b'' if query == '.' else query.encode('utf8')

        miner = manifest.miner(changeset)

        filt = request.filter
        if not filt:
            rx = None
        else:
            if len(filt) > SEARCH_FILES_FILTER_MAX_LENGTH:
                context.abort(StatusCode.INVALID_ARGUMENT,
                              "filter exceeds maximum length")
            # TODO what to do for invalid Regexp? Especially with incoming
            # format being Golang's
            try:
                rx = re.compile(filt.encode('utf8'))
            except re.error as exc:
                context.abort(StatusCode.INVALID_ARGUMENT,
                              f"filter did not compile: {exc})")

        start = request.offset
        end = None if request.limit == 0 else start + request.limit

        for paths in chunked(
                itertools.islice(
                    miner.file_names_by_regexp(rx, subdir),
                    start, end),
                force_if_empty=True,
        ):
            yield SearchFilesByNameResponse(files=paths)

    def SearchFilesByContent(self, request: SearchFilesByContentRequest,
                             context) -> SearchFilesByContentResponse:
        """Almost straight results from `git grep`

        this part of the protocol is totally undocumented, but here is what
        Gitaly does:

        - each match is sent with two lines of context before and after
        - in case of overlapping matches (including context), they are sent
          as one
        - sending a match means cutting it in chunkd of `WRITE_BUFFER_SIZE`.
        - after the full sending of each match aa  with the end_of_match`
          boolean set to true and no data is sent.

        (see also Comparison Tests for validatation of this).
        """
        repo = self.load_repo(request.repository, context)
        query = request.query
        if not query:
            context.abort(StatusCode.INVALID_ARGUMENT, "no query given")

        ref = request.ref
        changeset = gitlab_revision_changeset(repo, ref)
        if changeset is None:
            return

        # TODO filtermaxlen?
        rx = re.compile(query.encode('utf-8'), flags=re.IGNORECASE)
        # TODO chunked_response (not used by Rails app)
        match_data = BytesIO()
        miner = manifest.miner(changeset)
        for path, content, _flags in miner.iter_files_with_content(
                exclude_binary=True):
            # TODO rx options. Here's Gitaly reference (Golang), arguments
            # passed to `git grep`):
            # (with const surroundContext = 2)
            #
            #   git.Flag{Name: "--ignore-case"},
            #   git.Flag{Name: "-I"},
            #      (ignore binary files)
            #   git.Flag{Name: "--line-number"},
            #   git.Flag{Name: "--null"},
            #      (use null as delimiter between path, line number and
            #       matching line in the output, hence avoiding the need
            #       to escape)
            #   git.ValueFlag{Name: "--before-context",
            #                 Value: surroundContext},
            #   git.ValueFlag{Name: "--after-context", Value: surroundContext},
            #   git.Flag{Name: "--perl-regexp"},
            #   git.Flag{Name: "-e"},
            # Gitaly does not fill in `matches` field any more
            # (surely deprecated) and the Rails client does not read it
            # TODO cheaper iteration on a window of lines (note that
            # splitlines() takes care of `\r\n` and even `\r` EOLs.)
            for matching_lines in grep_file(rx, content):
                render_git_grep_matches(
                    match_data,
                    ref, path,
                    matching_lines)
                yield from iter_sfbc_resps(match_data)
                match_data.truncate(0)
                match_data.seek(0)

    def set_custom_hooks(self, request, context):
        def load_repo(req, context):
            return self.load_repo(req.repository, context)

        with streaming_request_tempfile_extract(
                request, context,
                first_request_handler=load_repo
        ) as (repo, tmpf):
            tmpf.flush()
            try:
                restore_additional(repo.ui, repo,
                                   tmpf.name.encode('ascii'))
            except Exception as exc:
                context.abort(StatusCode.INTERNAL,
                              "Error in tarball application: %r" % exc)

    def RestoreCustomHooks(self, request: RestoreCustomHooksRequest,
                           context) -> RestoreCustomHooksResponse:
        try:
            self.set_custom_hooks(request, context)
        finally:
            return RestoreCustomHooksResponse()

    def SetCustomHooks(self, request: SetCustomHooksRequest,
                       context) -> SetCustomHooksResponse:
        try:
            self.set_custom_hooks(request, context)
        finally:
            return SetCustomHooksResponse()

    def get_custom_hooks(self, request, context, resp_cls):
        repo = self.load_repo(request.repository, context)
        with tempfile.NamedTemporaryFile(
                mode='wb+',
                buffering=WRITE_BUFFER_SIZE) as tmpf:

            # TODO we should simply have backup_additional()
            # accept a file object rather than a path.
            save_path = pycompat.sysbytes(tmpf.name)
            backup_additional(repo.ui, repo, save_path)
            tmpf.seek(0)
            while True:
                data = tmpf.read(WRITE_BUFFER_SIZE)
                if not data:
                    break
                yield resp_cls(data=data)

    def BackupCustomHooks(self, request: BackupCustomHooksRequest,
                          context) -> BackupCustomHooksResponse:
        yield from self.get_custom_hooks(
            request, context, BackupCustomHooksResponse)

    def GetCustomHooks(self, request: GetCustomHooksRequest,
                       context) -> GetCustomHooksResponse:
        yield from self.get_custom_hooks(
            request, context, GetCustomHooksResponse)

    def RemoveRepository(self, request: RemoveRepositoryRequest,
                         context) -> RemoveRepositoryResponse:
        # The protocol comment says, as of Gitaly 14.8:
        #     RemoveRepository will move the repository to
        #     `+gitaly/tmp/<relative_path>_removed` and
        #     eventually remove it.
        # In that sentence, the "eventually" could imply that it is
        # asynchronous (as the Rails app does), but it is not in the
        # Gitaly server implementation. The renaming is done for
        # atomicity purposes.
        try:
            repo_path = self.repo_disk_path(request.repository, context)
        except KeyError as exc:
            self.handle_key_error(context, exc.args)
        except ValueError as exc:
            self.handle_value_error(context, exc.args)

        if not os.path.exists(repo_path):
            # same error message as Gitaly (probably no need to repeat
            # repo details, since request often logged client-side)
            context.abort(StatusCode.NOT_FOUND, "repository does not exist")

        trash_path = os.path.join(
            self.temp_dir(request.repository.storage_name, context),
            os.path.basename(repo_path) + b'+removed')
        # The rename being atomic, it avoids leaving a crippled repo behind
        # in case of problem in the removal.
        # TODO Gitaly also performs some kind of locking (not clear
        # if Mercurial locks would be appropriate because of the renaming)
        # and lengthy rechecks to safeguard against race conditions,
        # and finally the vote related to the multi-phase commit for praefect
        os.rename(repo_path, trash_path)

        shutil.rmtree(trash_path)  # not atomic
        return RemoveRepositoryResponse()

    def SetFullPath(self, request: SetFullPathRequest,
                    context) -> SetFullPathResponse:
        repo = self.load_repo(request.repository, context)

        if not request.path:
            context.abort(StatusCode.INVALID_ARGUMENT, "no path provided")

        set_gitlab_project_full_path(repo, request.path.encode('utf-8'))
        return SetFullPathResponse()

    def FullPath(self, request: FullPathRequest,
                 context) -> FullPathResponse:
        repo = self.load_repo(request.repository, context)

        path = get_gitlab_project_full_path(repo)
        if not path:  # None or (not probable) empty string
            # Gitaly simply returns the `git config` stderr output for now.
            # Pretty ridiculous to mimick it, we can hope not much to
            # depend on it.
            context.abort(StatusCode.INTERNAL, "Full path not set")
        return FullPathResponse(path=path)

    def CreateBundle(self, request: CreateBundleRequest,
                     context) -> CreateBundleResponse:
        repo = self.load_repo(request.repository, context).unfiltered()
        yield from self.gen_bundle_responses(CreateBundleResponse, repo,
                                             all=True)

    def gen_bundle_responses(self, response_class, repo, **bundle_opts):
        """Create bundle and generate gRPC responses"""
        # overrides makes sure that 1) phases info 2) obsmarkers are bundled
        overrides = {
            (b'experimental', b'bundle-phases'): True,
            (b'experimental', b'evolution.bundle-obsmarker'): True,
        }
        # also bundle the hidden changesets unless explicitely excluded
        bundle_opts.setdefault('hidden', True)
        with tempfile.NamedTemporaryFile(
                mode='wb+',
                buffering=WRITE_BUFFER_SIZE) as tmpf:
            try:
                with repo.ui.configoverride(overrides, b'CreateBundle'):
                    bundle(repo.ui, repo, pycompat.sysbytes(tmpf.name),
                           **bundle_opts)
            finally:
                gc.collect()
            tmpf.seek(0)
            while True:
                data = tmpf.read(WRITE_BUFFER_SIZE)
                if not data:
                    break
                yield response_class(data=data)

    def CreateBundleFromRefList(self, request: CreateBundleFromRefListRequest,
                                context) -> CreateBundleFromRefListResponse:
        # TODO Notes (probably for discussion only, before merging):
        # 1) Get it working for `git bundle create my.bundle master ^master~1`
        logger = LoggerAdapter(base_logger, context)
        first_req = next(request)
        repo_msg = first_req.repository
        if not (repo_msg.storage_name or repo_msg.relative_path):
            context.abort(StatusCode.INVALID_ARGUMENT, 'empty Repository')

        repo = self.load_repo(first_req.repository, context)
        patterns = itertools.chain(
            first_req.patterns,
            (pat for req in request for pat in req.patterns))

        incl_shas, excl_shas = resolve_revspecs_positive_negative(
            repo, patterns, ignore_unknown=True)
        logger.info("CreateBundleFromRefList repo=%r "
                    "included nodes=%r excluded nodes=%r",
                    message.Logging(first_req.repository),
                    incl_shas, excl_shas)

        # For info, in `hg bundle` one of the option from ('all', 'base')
        # is required, otherwise hg assumes that dest has all the nodes present
        incl_opts = {}
        if incl_shas is ALL_CHANGESETS:
            if not excl_shas:
                # underlying bundle command ignores --base if --all
                # is specified, but accepts --base without --rev, meaning
                # exactly what we need
                incl_opts['all'] = True
        else:
            incl_opts['rev'] = incl_shas

        if not excl_shas:
            excl_shas = [node.nullrev]

        yield from self.gen_bundle_responses(CreateBundleFromRefListResponse,
                                             repo.unfiltered(),
                                             base=excl_shas,
                                             **incl_opts)

    def FetchBundle(self, request: FetchBundleRequest,
                    context) -> FetchBundleResponse:
        logger = LoggerAdapter(base_logger, context)

        def load_or_init_repo(req, context):
            # TODO this should move to hgitaly.repository
            repo_path = self.repo_disk_path(req.repository, context)
            if os.path.lexists(repo_path):
                logger.info("FetchBundle: no need to create repo %r",
                            repo_path)
            else:
                self.hg_init_repository(req.repository, context)

            return self.load_repo(req.repository, context)

        try:
            with streaming_request_tempfile_extract(
                    request, context,
                    first_request_handler=load_or_init_repo
            ) as (repo, tmpf):
                unbundle(repo, tmpf.name)
        finally:
            gc.collect()
            return CreateRepositoryFromBundleResponse()

    def CreateRepositoryFromBundle(
            self, request: CreateRepositoryFromBundleRequest,
            context) -> CreateRepositoryFromBundleResponse:
        """Create repository from bundle.

        param `request`: is an iterator streaming sub-requests where first
        sub-request contains repository+data and subsequent sub-requests
        contains only data (i.e. the actual bundle sent in parts).
        """
        def init_repo(req, context):
            # TODO should move to hgitaly.repository
            self.hg_init_repository(req.repository, context)
            return self.load_repo(req.repository, context)

        with streaming_request_tempfile_extract(
                request, context,
                first_request_handler=init_repo
        ) as (repo, tmpf):
            try:
                unbundle(repo, tmpf.name)
            except Exception as exc:
                # same cleanup as Gitaly does, which gives later attempts
                # perhaps with a better bundle, chances to succeed.
                shutil.rmtree(repo.root)
                context.abort(StatusCode.INTERNAL,
                              "error in bundle application: %r" % exc)
            finally:
                gc.collect()
        return CreateRepositoryFromBundleResponse()

    def RemoveAll(self, request: RemoveAllRequest,
                  context) -> RemoveAllResponse:
        """Remove everything in the given storage.

        This is exactly what Gitaly v15.9 does, hence including all temporary
        files etc.
        """
        storage = request.storage_name
        root_dir = self.storages.get(storage)
        if root_dir is None:
            context.abort(
                StatusCode.INVALID_ARGUMENT,
                'remove all: GetStorageByName: '
                'no such storage: "%s"' % storage
            )

        root_dir = Path(os.fsdecode(root_dir)).resolve()
        # it would obviously be simpler to use shutil.rmtree() on root_dir
        # and recreate the storage afterwards *but*
        # - permission not guaranteed on the root dir
        # - risky on error recovery
        try:
            for sub in root_dir.iterdir():
                if sub.is_dir() and not sub.is_symlink():
                    shutil.rmtree(sub)
                else:
                    # also works with broken symlinks (even loops)
                    sub.unlink()
        except Exception as exc:
            context.abort(StatusCode.INTERNAL, "remove all: %s" % exc)
        return RemoveAllResponse()

    def hg_init_repository(self, repository: Repository, context):
        """Initialize a mercurial repository from a request object.

        :return: ``None``: the resulting repository has to be loaded in the
           standard way, using its path.
        :raises RepositoryCreationError: and updates context with error
           code and details.
        """
        logger = LoggerAdapter(base_logger, context)
        try:
            repo_path = self.repo_disk_path(repository, context)
        except KeyError:
            msg = "no such storage: %r" % repository.storage_name
            context.set_details(msg)
            logger.error(msg)
            context.set_code(StatusCode.INVALID_ARGUMENT)
            raise RepositoryCreationError(repository)

        if os.path.lexists(repo_path):
            msg = ("creating repository: repository exists already")
            context.set_details(msg)
            context.set_code(StatusCode.ALREADY_EXISTS)
            raise RepositoryCreationError(repository)

        try:
            logger.info("Creating repository at %r", repo_path)
            hg.peer(self.ui, opts={}, path=repo_path, create=True)
        except OSError as exc:
            context.set_code(StatusCode.INTERNAL)
            context.set_details("hg_init_repository(%r): %r" % (repo_path,
                                                                exc))
            raise RepositoryCreationError(repository)


def render_git_grep_matches(buf, ref, path, enum_lines):
    """Render a slice of lines as git grep does.

    :param enum_lines: iterable of pairs `(line_no, line)`
    """
    for lineno, line in enum_lines:
        buf.write(b'%s:%s\x00%d\x00%s\n' % (ref, path, lineno, line))


SPLITLINES_RX = re.compile(br'(.*?)(\r\n?|\n|\Z)', re.MULTILINE)


def grep_file(rx, data, context_width=2):
    """Iterator yielding matches the given regular expression with context

    This implementation avoids duplicating the data in memory.

    :param int context_width: number of lines before and after to include
      if possible (same as `grep -C`)
    :returns: pairs `(line_no, line)`
    """
    prev_match_line_no = None
    current_window = deque()  # current line and up to 2 lines before
    match_lines = []
    # According the the best ranked answer for
    # https://stackoverflow.com/questions/3054604,
    # this regexp-based splitting for lines can be a bit slower than
    # `iter(splitlines)` (things may have changes since then, though).
    # Yet, our biggest concern is to avoid exhausting HGitaly's RAM budget
    # if this happens to run on large files.
    # Unfortunately, we already have to load the entire data in RAM because
    # it is typically Mercurial file content, we don't want to do it once
    # more in the form of lines. In both cases a bytes string
    # is allocated for each line, but that is harder to prevent and they
    # should be deallocated at each iteration (no cycles).
    # Unless there is a bug in the current approach, it is not worth the
    # effort to try and further improve memory efficiency: implementing
    # in RHGitaly would be the way to go.
    for line_idx, line_m in enumerate(SPLITLINES_RX.finditer(data)):
        line = line_m.group(1)
        if not line:
            continue
        line_no = line_idx + 1
        current_window.append((line_no, line))
        if rx.search(line):
            if (
                    prev_match_line_no is None
                    or line_no - prev_match_line_no > 2 * context_width
            ):
                match_lines = list(current_window)
            else:
                match_lines.append((line_no, line))
            prev_match_line_no = line_no
        elif (
                prev_match_line_no is not None
                and line_no <= prev_match_line_no + context_width
        ):
            match_lines.append((line_no, line))
        elif match_lines:
            yield match_lines
            match_lines = []

        if len(current_window) > context_width:
            current_window.popleft()
    if match_lines:
        yield match_lines


def iter_sfbc_resps(match_data: BytesIO):
    """Yield SearchFilesByContentResponse messages for the given match_data.
    """
    value = match_data.getvalue()
    match_len = len(value)
    sent = 0  # actually rounded to the upper WRITE_BUFFER_SIZE
    while sent < match_len:
        yield SearchFilesByContentResponse(
            match_data=value[sent:sent + WRITE_BUFFER_SIZE])
        sent += WRITE_BUFFER_SIZE

    match_data.truncate(0)
    match_data.seek(0)
    yield SearchFilesByContentResponse(end_of_match=True)
