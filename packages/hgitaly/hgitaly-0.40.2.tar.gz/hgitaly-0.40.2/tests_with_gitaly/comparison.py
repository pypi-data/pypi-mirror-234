# Copyright 2020 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
"""Fixture for Gitaly comparison tests based on Heptapod's Git mirroring."""
import attr
import contextlib
from copy import deepcopy
import functools
import pytest
import random

import grpc

from mercurial_testhelpers.util import as_bytes

from hggit.git_handler import GitHandler
from heptapod.testhelpers.gitlab import GitLabMirrorFixture
from hgext3rd.heptapod.keep_around import (
    create_keep_around,
)
from hgext3rd.heptapod.special_ref import (
    write_gitlab_special_ref,
    special_refs,
)
from hgitaly import feature
from hgitaly.gitlab_ref import (
    keep_around_ref_path,
)
from hgitaly.stub.shared_pb2 import Repository


@attr.s
class GitalyComparison:
    hgitaly_channel = attr.ib()
    gitaly_channel = attr.ib()
    gitaly_repo = attr.ib()
    hgitaly_repo = attr.ib()
    gitlab_mirror = attr.ib()
    rhgitaly_channel = attr.ib(default=None)

    @property
    def hg_repo_wrapper(self):
        return self.gitlab_mirror.hg_repo_wrapper

    @property
    def git_repo(self):
        return self.gitlab_mirror.git_repo

    def rpc_helper(self, **kw):
        return RpcHelper(self, **kw)

    @functools.cached_property
    def hg_git(self):
        """The hg-git GitHandler instance, with SHA mapping preloaded.

        To invalidate this cached property, use :meth:`invalidate`
        """
        hg_repo = self.hg_repo_wrapper.repo
        hg_git = GitHandler(hg_repo, hg_repo.ui)
        hg_git.load_map()
        return hg_git

    def invalidate(self):
        """Invalidate all caches.

        In particular, reload the Mercurial repo
        """
        try:
            del self.hg_git
        except AttributeError:
            # the cached property has not been used yet, nothing to do
            pass

        self.hg_repo_wrapper.reload()
        self.gitlab_mirror.activate_mirror()

    def write_special_ref(self, ref_name, hg_sha):
        """Write a special ref in both repos

        :param ref_name: the special ref name (without `refs/`)
        :param bytes hg_sha: hexadecimal Mercurial Node ID of the changeset
          to point to

        :return: a pair of :class:`bytes` instance: (full ref path, git_sha)
        """
        git_sha = self.hg_git.map_git_get(hg_sha)
        if git_sha is None:
            raise LookupError("Git commit not found for %r" % hg_sha)

        hg_wrapper = self.hg_repo_wrapper
        git_repo = self.git_repo

        ref_path = b'refs/' + ref_name
        self.git_repo.write_ref(ref_path.decode(), git_sha)
        write_gitlab_special_ref(hg_wrapper.repo, ref_name, hg_sha)
        hg_wrapper.reload()
        assert ref_path in git_repo.all_refs()
        assert ref_name in special_refs(hg_wrapper.repo)
        return ref_path, git_sha

    def create_keep_around(self, hg_sha):
        """Create a keep-around ref in both repos

        :param bytes hg_sha: hexadecimal Mercurial Node ID of the changeset
          to point to

        On the Git side, the keep-around is set for the Git commit
        corresponding to the Mercurial commit.

        :return: a pair of :class:`bytes` instances:
          (full Mercurial ref path, full Git ref path)
        """
        git_sha = self.hg_git.map_git_get(hg_sha)
        hg_wrapper = self.hg_repo_wrapper
        git_repo = self.git_repo

        hg_ref_path = keep_around_ref_path(hg_sha)
        git_ref_path = keep_around_ref_path(git_sha)

        create_keep_around(hg_wrapper.repo, hg_sha)
        git_repo.write_ref(git_ref_path, git_sha)
        hg_wrapper.reload()
        return hg_ref_path, git_ref_path


@contextlib.contextmanager
def gitaly_comparison_fixture(server_repos_root,
                              gitaly_channel,
                              grpc_channel,
                              monkeypatch,
                              rhgitaly_channel=None,
                              ):
    common_relative_path = 'repo-' + hex(random.getrandbits(64))[2:]
    storage = 'default'

    gitaly_repo = Repository(relative_path=common_relative_path + '.git',
                             storage_name=storage)
    hgitaly_repo = Repository(relative_path=common_relative_path + '.hg',
                              storage_name=storage)

    hg_config = dict(phases=dict(publish=False),
                     ui=dict(username='Hgitaly Tests <hgitaly@heptapod.test>'),
                     extensions={name: '' for name in ('evolve',
                                                       'hggit',
                                                       'topic',
                                                       'hgitaly',
                                                       'heptapod')})
    with GitLabMirrorFixture.init(
            server_repos_root / storage,
            monkeypatch,
            common_repo_name=common_relative_path,
            hg_config=hg_config,
    ) as mirror:
        # configuration must be written in HGRC file, because
        # HGitaly server will load the repository independently.
        mirror.hg_repo_wrapper.write_hgrc(hg_config)
        mirror.activate_mirror()
        yield GitalyComparison(
            hgitaly_channel=grpc_channel,
            hgitaly_repo=hgitaly_repo,
            gitaly_channel=gitaly_channel,
            rhgitaly_channel=rhgitaly_channel,
            gitaly_repo=gitaly_repo,
            gitlab_mirror=mirror,
        )


class BaseRpcHelper:
    """Common helper for all comparisons.

    Will handle comparison between Gitaly and (HGitaly or HGitaly) as well
    as comparison beween HGitaly and RHGitaly, or whatever comes next.
    """

    def __init__(self, comparison, stub_cls, method_name, request_cls,
                 repository_arg=True,
                 request_defaults=None,
                 feature_flags=(),
                 streaming=False):
        self.comparison = comparison
        self.stub_cls = stub_cls
        self.method_name = method_name
        self.request_cls = request_cls
        self.streaming = streaming
        self.repository_arg = repository_arg

        self.request_defaults = request_defaults
        self.streaming = streaming
        self.feature_flags = list(feature_flags)

        self.init_stubs()

    def init_stubs(self):
        """To be provided by subclasses."""
        raise NotImplementedError  # pragma no cover

    def grpc_metadata(self):
        return feature.as_grpc_metadata(self.feature_flags)

    def rpc(self, backend, **kwargs):
        if self.repository_arg:
            kwargs.setdefault('repository', self.comparison.gitaly_repo)
        request = self.request_cls(**kwargs)
        meth = getattr(self.stubs[backend], self.method_name)
        metadata = self.grpc_metadata()
        if self.streaming:
            return [resp for resp in meth(request, metadata=metadata)]

        return meth(request, metadata=metadata)

    def apply_request_defaults(self, kwargs):
        defaults = self.request_defaults
        if defaults is not None:
            for k, v in defaults.items():
                kwargs.setdefault(k, v)


class RpcHelper(BaseRpcHelper):
    """Encapsulates a comparison fixture with call and compare helpers.

    As Mercurial and Git responses are expected to differ (commit hashes and
    the like), this class provides a uniform mechanism to account for
    the expected difference, before finally asserting equality of
    the responses.

    # TODO much more to document.

    :attr:`feature_flags`: a mutable list of pairs such as
      ``(`my-flag`, True)``. The flags are sent to both servers.
    :attr:`response_sha_attrs`: Used to specify response attributes to
      convert to Git for comparison. See :meth:`attr_path_to_git` for
      specification.
    """

    def __init__(self, comparison, stub_cls, method_name, request_cls,
                 hg_server='hgitaly',
                 request_sha_attrs=(),
                 response_sha_attrs=(),
                 normalizer=None,
                 error_details_normalizer=None,
                 chunked_fields_remover=None,
                 chunks_concatenator=None,
                 **kwargs,
                 ):
        self.hg_server = hg_server
        super(RpcHelper, self).__init__(
            comparison, stub_cls, method_name, request_cls,
            **kwargs
        )
        self.request_sha_attrs = request_sha_attrs
        self.response_sha_attrs = response_sha_attrs
        self.normalizer = normalizer
        self.error_details_normalizer = error_details_normalizer
        self.chunked_fields_remover = chunked_fields_remover
        self.chunks_concatenator = chunks_concatenator

    def init_stubs(self):
        comparison, stub_cls = self.comparison, self.stub_cls

        if self.hg_server == 'rhgitaly':
            hg_channel = comparison.rhgitaly_channel
        else:
            hg_channel = comparison.hgitaly_channel
        self.stubs = dict(git=stub_cls(comparison.gitaly_channel),
                          hg=stub_cls(hg_channel))

    def hg2git(self, hg_sha):
        """Convert a Mercurial hex SHA to its counterpart SHA in Git repo.

        If not found in the Git Repo, the original SHA is returned, which
        is useful for tests about non existent commits.
        """
        # if hg_sha is None or not 40 bytes long it certainly won't
        # be found in the hg-git mapping, we don't need a special case
        # for that
        git_sha = self.comparison.hg_git.map_git_get(as_bytes(hg_sha))
        return hg_sha if git_sha is None else git_sha

    def request_kwargs_to_git(self, hg_kwargs):
        git_kwargs = hg_kwargs.copy()
        for sha_attr in self.request_sha_attrs:
            sha = hg_kwargs.get(sha_attr)
            if sha is None:
                continue
            if isinstance(sha, list):
                git_kwargs[sha_attr] = [self.revspec_to_git(s) for s in sha]
            else:
                git_kwargs[sha_attr] = self.revspec_to_git(sha)
        return git_kwargs

    def revspec_to_git(self, revspec):
        """Convert revision specifications, including ranges to Git.

        This is to be improved as new cases arise.
        """
        is_bytes = isinstance(revspec, bytes)
        symdiff_sep = b'...' if is_bytes else '...'
        only_sep = b'..' if is_bytes else '..'

        for sep in (symdiff_sep, only_sep):
            if sep in revspec:
                # hg2git() defaulting rule will let symbolic revisions, such
                # as refs go through untouched
                return sep.join(self.hg2git(rev)
                                for rev in revspec.split(sep))
        # TODO implement caret, tilda etc.
        return self.hg2git(revspec)

    def response_to_git(self, resp):
        sha_attr_paths = [path.split('.') for path in self.response_sha_attrs]
        if self.streaming:
            for message in resp:
                self.message_to_git(message, sha_attr_paths)
        else:
            self.message_to_git(resp, sha_attr_paths)

    def message_to_git(self, message, attr_paths):
        for attr_path in attr_paths:
            self.attr_path_to_git(message, attr_path)

    def attr_path_to_git(self, message, attr_path):
        """Convert to Git part of message specified by an attr_path.

        :param attr_path: symbolic representation, as a succession of dotted
          attribute names. In case an attribute name ends with ``[]``, it
          is expected to be a simple list on which to iterate.
          Examples:
          - ``id``: convert ``message.id``
          - ``commits[].id``: for each element ``c`` of ``message.commits``,
            convert  ``c.id``
          - ``commits[].parent_ids[]`: for each element ``c`` of
            ``message.commits``, convert  all values in ``c.parent_ids``
        """
        obj = message
        trav = list(attr_path)
        while len(trav) > 1:
            attr_name, trav = trav[0], trav[1:]
            recurse = attr_name.endswith('[]')
            if recurse:
                attr_name = attr_name[:-2]
            # HasField cannot be used on repeated attributes, hence the elif
            elif not obj.HasField(attr_name):
                return
            obj = getattr(obj, attr_name)
            if recurse:
                for msg in obj:
                    self.message_to_git(msg, [trav])
                return

        obj_attr = trav[0]
        scalar_list = obj_attr.endswith('[]')
        if scalar_list:
            obj_attr = obj_attr[:-2]
        value = getattr(obj, obj_attr)

        if scalar_list:
            for i, sha in enumerate(value):
                value[i] = self.hg2git(sha)
        else:
            setattr(obj, obj_attr, self.hg2git(value))

    def call_backends(self, **hg_kwargs):
        """Call Gitaly and HGitaly with uniform request kwargs.

        To be used only if no error is expected.

        :param hg_kwargs: used as-is to construct the request for HGitaly,
          converted to Git and then to a request for Gitaly.
        """
        self.apply_request_defaults(hg_kwargs)

        git_kwargs = self.request_kwargs_to_git(hg_kwargs)

        hg_response = self.rpc('hg', **hg_kwargs)
        git_response = self.rpc('git', **git_kwargs)

        return hg_response, git_response

    def normalize_responses(self, hg_response, git_response):
        self.response_to_git(hg_response)
        norm = self.normalizer
        if norm is not None:
            norm(self, hg_response, vcs='hg')
            norm(self, git_response, vcs='git')

    def assert_compare(self, **hg_kwargs):
        hg_response, git_response = self.call_backends(**hg_kwargs)
        self.normalize_responses(hg_response, git_response)
        assert hg_response == git_response

    def assert_compare_aggregated(self,
                                  compare_first_chunks=True,
                                  check_both_chunked=True,
                                  **hg_kwargs):
        """Compare streaming responses with appropriate concatenation.

        Sometimes, it's unreasonable to expect HGitaly chunking to
        exactly match Gitaly's. This method allows to compare after
        regrouping the chunks, with the provided :attr:`chunks_concatenator`.

        Usually Gitaly returns small values within the first response only,
        to avoid the bandwidth waste of repetiting them. This helper
        checks that HGitaly does the same by comparing after applying
        :attr: `chunked_fields_remover` to as many responses as possible
        (typically the number of responses would differ).

        :param bool compare_first_chunk: if ``True``, the first chunks of
          both responses are directly compared (including main content). If
          ``False``, they are still compared, just ignoring main content.
        :param bool check_both_chunked: if ``True` checks that we get
          more than one response for both HGitaly and Gitaly
        :return: a pair: the first chunk of responses for Gitaly and HGitaly
          respectively, taken before normalization. This can be useful, e.g.,
          for pagination parameters.
        """
        assert self.streaming  # for consistency

        hg_resps, git_resps = self.call_backends(**hg_kwargs)
        original_first_chunks = deepcopy((git_resps[0], hg_resps[0]))

        self.normalize_responses(hg_resps, git_resps)
        if compare_first_chunks:
            assert hg_resps[0] == git_resps[0]

        if check_both_chunked:
            assert len(hg_resps) > 1
            assert len(git_resps) > 1

        concatenator = getattr(self, 'chunks_concatenator')
        fields_remover = getattr(self, 'chunked_fields_remover')
        assert concatenator(hg_resps) == concatenator(git_resps)

        for hg_resp, git_resp in zip(hg_resps, git_resps):
            if fields_remover is not None:
                fields_remover(hg_resp)
                fields_remover(git_resp)
            assert hg_resp == git_resp

        return original_first_chunks

    def assert_compare_errors(self, same_details=True, **hg_kwargs):
        self.apply_request_defaults(hg_kwargs)

        git_kwargs = self.request_kwargs_to_git(hg_kwargs)
        with pytest.raises(grpc.RpcError) as exc_info_hg:
            self.rpc('hg', **hg_kwargs)
        with pytest.raises(grpc.RpcError) as exc_info_git:
            self.rpc('git', **git_kwargs)
        exc_hg = exc_info_hg.value
        exc_git = exc_info_git.value

        assert exc_hg.code() == exc_git.code()
        if same_details:
            norm = self.error_details_normalizer
            hg_details = exc_hg.details()
            git_details = exc_git.details()
            if norm is not None:  # pragma no cover
                hg_details = norm(hg_details, vcs='hg')
                git_details = norm(git_details, vcs='git')
            assert hg_details == git_details

        # trailing metadata can bear a typed error gRPC message, which
        # is more important to compare than "details" (in the sense of
        # human-readable message), so let's check them unconditionally:
        # TODO check how to unskew that: RHGitaly currently adds
        # `content-length` and `date`, which Gitaly does not
        md_hg = dict(exc_hg.trailing_metadata())
        md_hg.pop('content-length', None)
        md_hg.pop('date', None)
        md_git = dict(exc_git.trailing_metadata())
        assert md_hg == md_git

        return exc_hg, exc_git


def normalize_commit_message(commit):
    """Remove expected differences between commits in Gitaly and HGitaly.

    Some are really testing artifacts, some have eventually to be removed.
    """
    # TODO tree_id should be replaced by HGitaly standard value
    # once HGitaly2 is the norm
    commit.tree_id = ''

    # hg-git may add a branch marker (this is just a test artifact)
    hg_marker = b'\n--HG--\n'
    split = commit.body.split(hg_marker, 1)
    if len(split) > 1:
        commit.body = split[0]
        commit.body_size = commit.body_size - len(split[1]) - len(hg_marker)

    # Either hg-git or Git itself adds a newline if there isn't one.
    # TODO investigate and if it is Git, add the newline in Mercurial
    # response.
    if not commit.body.endswith(b'\n'):
        commit.body = commit.body + b'\n'
        commit.body_size = commit.body_size + 1
