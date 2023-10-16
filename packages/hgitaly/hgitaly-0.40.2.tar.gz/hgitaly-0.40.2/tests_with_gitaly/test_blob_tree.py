# Copyright 2021 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
from copy import deepcopy
import pytest

from hgitaly.oid import (
    blob_oid,
    tree_oid,
)
from hgitaly.revision import (
    gitlab_revision_changeset,
    ZERO_SHA,
    ZERO_SHA_STR,
)
from hgitaly.stream import WRITE_BUFFER_SIZE

from hgitaly.stub.shared_pb2 import (
    PaginationParameter,
    Repository,
)
from hgitaly.stub.blob_pb2 import (
    GetBlobRequest,
    GetBlobsRequest,
)
from hgitaly.stub.commit_pb2 import (
    GetTreeEntriesRequest,
    TreeEntryRequest,
)
from hgitaly.stub.blob_pb2_grpc import BlobServiceStub
from hgitaly.stub.commit_pb2_grpc import CommitServiceStub

from . import skip_comparison_tests
if skip_comparison_tests():  # pragma no cover
    pytestmark = pytest.mark.skip

parametrize = pytest.mark.parametrize


def concat_data_fields(responses):
    """Callback for RpcHelper.assert_compare_aggregated.

    Works for all response gRPC messages with a `data` field.
    """
    return b''.join(r.data for r in responses)


def remove_data_field(response):
    """Callback for RpcHelper.assert_compare_aggregated.

    Allows to compare all fields but `data`.
    """
    response.data = b''


def oid_mapping(gitaly_comp, rev_paths):
    """Provide the OID mappings between Mercurial and Git for blobs.

    :param fixture: an instance of `GitalyComparison`
    :param rev_paths: an iterable of tuples (revision, path, type), where
      type is 'tree' or 'blob'
    :return: a :class:`dict` mapping Mercurial oids to Git oids

    Does not need HGitaly blob/tree methods to work, only those of Gitaly.
    """
    res = {}
    gitaly_meth = CommitServiceStub(gitaly_comp.gitaly_channel).TreeEntry
    hg_repo = gitaly_comp.hg_repo_wrapper.repo
    hg_oid_meths = dict(tree=tree_oid, blob=blob_oid)
    for rev, path, t in rev_paths:
        changeset = gitlab_revision_changeset(hg_repo, rev)
        hg_oid = hg_oid_meths[t](hg_repo, changeset.hex().decode(), path)
        gitaly_resp = gitaly_meth(
            TreeEntryRequest(repository=gitaly_comp.gitaly_repo,
                             revision=rev,
                             path=path,
                             limit=1)
        )
        res[hg_oid] = next(iter(gitaly_resp)).oid
    return res


def oid_normalizer(oid2git):
    """Return a response normalizer for oid fields.

    :param oid_mapping: :class:`dict` instance mapping HGitaly OIDs to
      Gitaly OIDs
    """
    def normalizer(rpc_helper, responses, vcs='hg'):
        if vcs != 'hg':
            return

        for entry in responses:
            if entry.oid:
                entry.oid = oid2git[entry.oid]

    return normalizer


@parametrize('hg_server', ('hgitaly', 'rhgitaly'))
def test_compare_tree_entry_request(gitaly_rhgitaly_comparison, hg_server):
    fixture = gitaly_rhgitaly_comparison

    wrapper = fixture.hg_repo_wrapper
    wrapper.write_commit('foo', message="Some foo")
    sub = (wrapper.path / 'sub')
    sub.mkdir()
    (sub / 'bar').write_text('bar content')
    (sub / 'ba2').write_text('ba2 content')
    # TODO OS indep for paths (actually TODO make wrapper.commit easier to
    # use, e.g., check how to make it accept patterns)
    wrapper.commit(rel_paths=['sub/bar', 'sub/ba2'],
                   message="zebar", add_remove=True)

    default_rev = b'branch/default'
    oid2git = oid_mapping(fixture,
                          ((default_rev, b'foo', 'blob'),
                           (default_rev, b'sub', 'tree'),
                           (default_rev, b'sub/bar', 'blob'),
                           (default_rev, b'sub/ba2', 'blob'),
                           ))
    normalizer = oid_normalizer(oid2git)

    rpc_helper = fixture.rpc_helper(stub_cls=CommitServiceStub,
                                    hg_server=hg_server,
                                    method_name='TreeEntry',
                                    request_cls=TreeEntryRequest,
                                    request_defaults=dict(
                                        revision=default_rev,
                                        limit=0,
                                        max_size=0),
                                    streaming=True,
                                    normalizer=normalizer,
                                    chunked_fields_remover=remove_data_field,
                                    chunks_concatenator=concat_data_fields,
                                    )
    assert_compare = rpc_helper.assert_compare
    assert_compare_errors = rpc_helper.assert_compare_errors

    # precondition for the test: mirror worked
    assert fixture.git_repo.branch_titles() == {default_rev: b"zebar"}

    # basic case
    for path in (b'sub', b'sub/bar', b'sub/'):
        assert_compare(path=path)

    for path in (b'.', b'do-not-exist'):
        assert_compare_errors(path=path)

    # limit and max_size (does not apply to Trees)
    assert_compare(path=b'foo', limit=4)
    assert_compare_errors(path=b'foo', max_size=4)
    assert_compare(path=b'sub', max_size=1)

    # unknown revision
    assert_compare_errors(path=b'sub', revision=b'unknown')
    assert_compare_errors(path=b'sub', revision=ZERO_SHA)

    # chunking for big Blob entry
    wrapper.write_commit('bigfile', message="A big file with 2 or 3 chunks",
                         content=b'a' * 1023 + b'ff' * 65536)
    # default_rev now resolves to another changeset, hence a different
    # HGitaly OID given the current implementation
    oid2git.update(oid_mapping(fixture, ((default_rev, b'bigfile', 'blob'),
                                         (default_rev, b'sub', 'tree'),
                                         (default_rev, b'sub/bar', 'blob'),
                                         (default_rev, b'sub/ba2', 'blob'),
                                         (default_rev, b'foo', 'blob'),
                                         )))
    rpc_helper.assert_compare_aggregated(path=b'bigfile',
                                         compare_first_chunks=False)

    #
    # reusing content to test GetTreeEntries, hence with a new rpc_helper
    #

    def gte_normalizer(rpc_helper, responses, vcs='hg'):
        for resp in responses:
            for entry in resp.entries:
                if entry.oid and vcs == 'hg':
                    entry.oid = oid2git[entry.oid]
                entry.root_oid = b''

    rpc_helper = fixture.rpc_helper(stub_cls=CommitServiceStub,
                                    hg_server=hg_server,
                                    method_name='GetTreeEntries',
                                    request_cls=GetTreeEntriesRequest,
                                    request_defaults=dict(
                                        revision=default_rev,
                                        ),
                                    streaming=True,
                                    normalizer=gte_normalizer,
                                    )
    assert_compare = rpc_helper.assert_compare

    for path in (b'.', b'sub'):
        for recursive in (False, True):
            for skip_flat in (False, True):
                assert_compare(path=path,
                               skip_flat_paths=skip_flat,
                               recursive=recursive)

    assert_compare(path=b'.', revision=b'unknown')

    # case when path is actually a file
    assert_compare(path=b'sub/bar')

    # sort parameter
    SortBy = GetTreeEntriesRequest.SortBy
    for recursive in (False, True):
        assert_compare(path=b'.', recursive=recursive,
                       sort=SortBy.TREES_FIRST)

    # tree first and nested trees
    nested = sub / 'nested'
    nested.mkdir()
    (nested / 'deeper').write_text('deep thoughts')
    wrapper.commit_file('sub/nested/deeper', message='deeper')
    assert fixture.git_repo.branch_titles() == {b'branch/default': b"deeper"}

    # see comment above about update of OID mapping
    oid2git.update(oid_mapping(fixture, (
        (default_rev, b'bigfile', 'blob'),
        (default_rev, b'sub', 'tree'),
        (default_rev, b'sub/bar', 'blob'),
        (default_rev, b'sub/ba2', 'blob'),
        (default_rev, b'sub/nested', 'tree'),
        (default_rev, b'sub/nested/deeper', 'blob'),
        (default_rev, b'foo', 'blob'),
    )))
    for skip_flat in (False, True):
        assert_compare(path=b'.',
                       recursive=True,
                       skip_flat_paths=skip_flat,
                       sort=SortBy.TREES_FIRST)


@parametrize('hg_server', ('hgitaly', 'rhgitaly'))
def test_compare_get_tree_entries_pagination(gitaly_rhgitaly_comparison,
                                             hg_server):
    fixture = gitaly_rhgitaly_comparison

    wrapper = fixture.hg_repo_wrapper
    wrapper.write_commit('foo', message="Some foo")
    sub = (wrapper.path / 'sub')
    sub.mkdir()
    rel_paths = []
    # Chunk size with Gitaly is big
    for x in range(2900):
        # max file name length is 255 on most filesystems
        path = sub / ('very-' * 46 + '-long-filename-bar%04d' % x)
        path.write_text(str(x))
        rel_paths.append(path)
    # TODO OS indep for paths (actually TODO make wrapper.commit easier to
    # use, e.g., check how to make it accept patterns)
    wrapper.commit(rel_paths=rel_paths,
                   message="zebar", add_remove=True)

    def normalizer(rpc_helper, responses, **kw):
        for resp in responses:
            for entry in resp.entries:
                entry.oid = entry.root_oid = b''
            resp.pagination_cursor.next_cursor = ''

    def concat_entries(responses):
        return list(e for r in responses for e in r.entries)

    def remove_entries(response):
        del response.entries[:]

    cursor2git = {}  # hg cursor -> git cursor

    rpc_helper = fixture.rpc_helper(stub_cls=CommitServiceStub,
                                    hg_server=hg_server,
                                    method_name='GetTreeEntries',
                                    request_cls=GetTreeEntriesRequest,
                                    request_defaults=dict(
                                        revision=b'branch/default',
                                    ),
                                    streaming=True,
                                    normalizer=normalizer,
                                    chunked_fields_remover=remove_entries,
                                    chunks_concatenator=concat_entries,
                                    )

    def request_kwargs_to_git(hg_kwargs):
        """Swapping the cursor is too specific for the current RpcHelper.

        We might grow something for all paginated methods, though.
        """
        pagination = hg_kwargs.get('pagination_params')
        if pagination is None:
            return hg_kwargs

        hg_cursor = pagination.page_token
        if not hg_cursor:
            return hg_kwargs

        git_kwargs = deepcopy(hg_kwargs)
        git_kwargs['pagination_params'].page_token = cursor2git[hg_cursor]
        return git_kwargs

    rpc_helper.request_kwargs_to_git = request_kwargs_to_git

    assert_compare = rpc_helper.assert_compare
    assert_compare_aggregated = rpc_helper.assert_compare_aggregated

    # asking more than the expected Gitaly first chunk size (2888 entries)
    # but still less than the total
    first_resps = assert_compare_aggregated(
        path=b'sub',
        recursive=True,
        pagination_params=PaginationParameter(limit=2890),
        compare_first_chunks=False,
    )

    git_cursor, hg_cursor = [resp.pagination_cursor.next_cursor
                             for resp in first_resps]
    assert git_cursor
    assert hg_cursor
    cursor2git[hg_cursor] = git_cursor

    # using the cursor
    assert_compare(path=b'sub',
                   recursive=True,
                   pagination_params=PaginationParameter(page_token=hg_cursor,
                                                         limit=9000))

    # negative limit means all results, and there's no cursor if no next page
    git_resp0, hg_resp0 = assert_compare_aggregated(
        path=b'sub',
        recursive=True,
        pagination_params=PaginationParameter(limit=-1),
        compare_first_chunks=False,
    )
    assert git_resp0.pagination_cursor == hg_resp0.pagination_cursor

    # case of limit=0 (empty results)
    assert_compare(path=b'sub',
                   recursive=True,
                   pagination_params=PaginationParameter(limit=0),
                   )

    # case of unknown revision and limit=0
    assert_compare(path=b'.', revision=b'unknown',
                   pagination_params=PaginationParameter(limit=0))

    # case of no pagination params
    assert_compare_aggregated(path=b'sub',
                              recursive=True,
                              compare_first_chunks=False)

    # case of a cursor that doesn't match any entry (can happen if content
    # changes between requests)
    cursor = "surely not an OID"
    cursor2git[cursor] = cursor
    rpc_helper.assert_compare_errors(path=b'sub',
                                     recursive=True,
                                     pagination_params=PaginationParameter(
                                         page_token=cursor,
                                         limit=10)
                                     )


def rev_path_messages(rev_paths):
    """Convert (revision, path) pairs into a list of `RevisionPath` messages.
    """
    return [GetBlobsRequest.RevisionPath(revision=rev, path=path)
            for rev, path in rev_paths]


@parametrize('hg_server', ('hgitaly', 'rhgitaly'))
def test_compare_get_blob_request(gitaly_rhgitaly_comparison, hg_server):
    fixture = gitaly_rhgitaly_comparison
    git_repo = fixture.git_repo

    wrapper = fixture.hg_repo_wrapper
    large_data = b'\xbe' * WRITE_BUFFER_SIZE + b'\xefdata'

    wrapper.commit_file('small', message="Small file")
    changeset = wrapper.commit_file('foo', message="Large foo",
                                    content=large_data)
    hg_sha = changeset.hex().decode()
    hg_oid = blob_oid(wrapper.repo, hg_sha, b'foo')

    default_rev = b'branch/default'

    # mirror worked
    assert git_repo.branch_titles() == {default_rev: b"Large foo"}

    oid2git = oid_mapping(fixture,
                          ((default_rev, b'foo', 'blob'),
                           (default_rev, b'small', 'blob')))
    normalizer = oid_normalizer(oid2git)

    rpc_helper = fixture.rpc_helper(stub_cls=BlobServiceStub,
                                    hg_server=hg_server,
                                    method_name='GetBlob',
                                    request_cls=GetBlobRequest,
                                    request_defaults=dict(
                                        limit=-1,
                                    ),
                                    streaming=True,
                                    normalizer=normalizer,
                                    chunked_fields_remover=remove_data_field,
                                    chunks_concatenator=concat_data_fields,
                                    )

    def request_kwargs_to_git(hg_kwargs):
        """Swapping oid is too specific for the current RpcHelper

        We might provide it with a direct `git` subprocess or with dulwich,
        though.
        """
        git_kwargs = deepcopy(hg_kwargs)
        git_kwargs['oid'] = oid2git[hg_kwargs['oid']]
        return git_kwargs

    rpc_helper.request_kwargs_to_git = request_kwargs_to_git

    rpc_helper.assert_compare(oid=hg_oid, limit=12)
    rpc_helper.assert_compare(oid=hg_oid, limit=0)
    for cs, path in (('12de34ad' * 5, b'foo'),
                     (ZERO_SHA_STR, b'irrelevant/path'),
                     (hg_sha, b'unknown-file'),
                     ):
        unknown_oid = blob_oid(wrapper.repo, cs, path)
        oid2git[unknown_oid] = unknown_oid
        rpc_helper.assert_compare(oid=unknown_oid)

    rpc_helper.assert_compare_aggregated(oid=hg_oid,
                                         compare_first_chunks=False)

    oid2git[''] = ''
    rpc_helper.assert_compare_errors(repository=None, oid='',
                                     # details differ just by capitalization
                                     # as of this writing
                                     same_details=False,
                                     )
    rpc_helper.assert_compare_errors(oid='')
    bogus_repos = (Repository(storage_name='unknown',
                              relative_path='some_path'),
                   Repository(storage_name=fixture.gitaly_repo.storage_name,
                              relative_path='does/not/exist'),
                   None,
                   )

    for repo in bogus_repos:
        rpc_helper.assert_compare_errors(repository=repo,
                                         oid=hg_oid,
                                         same_details=False)

    # now with GetBlobs
    rpc_helper = fixture.rpc_helper(stub_cls=BlobServiceStub,
                                    hg_server=hg_server,
                                    method_name='GetBlobs',
                                    request_cls=GetBlobsRequest,
                                    request_defaults=dict(
                                        limit=-1,
                                    ),
                                    streaming=True,
                                    normalizer=normalizer,
                                    chunked_fields_remover=remove_data_field,
                                    chunks_concatenator=concat_data_fields,
                                    )

    rev_paths = rev_path_messages(((b'branch/default', b'small'),
                                   (b'branch/default', b'does-not-exist'),
                                   (b'no-such-revision', b'small'),
                                   (ZERO_SHA_STR, b'irrelevant/path'),
                                   ))
    rpc_helper.assert_compare(revision_paths=rev_paths)
    # with limits (the limit is per file)
    # the case of limit=0 is important, being used by the Rails app to
    # obtain metadata only (see e.g., `BlobService.get_blob_types`).
    for limit in (0, 3):
        rpc_helper.assert_compare(revision_paths=rev_paths, limit=limit)

    # chunking in get_blobs, again non-deterministic for Gitaly
    rev_paths = rev_path_messages(((b'branch/default', b'small'),
                                   (b'branch/default', b'foo'),
                                   ))
    rpc_helper.assert_compare_aggregated(revision_paths=rev_paths)

    # corner cases
    for repo in bogus_repos:
        rpc_helper.assert_compare_errors(repository=repo,
                                         revision_paths=rev_paths,
                                         same_details=False)
