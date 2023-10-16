# Copyright 2021 Sushil Khanchi <sushilkhanchi97@gmail.com>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
from mercurial import (
    node as node_mod,
    pycompat,
)
import pytest
import grpc
import itertools
# from hgitaly.git import EMPTY_TREE_OID
from hgitaly.stub.shared_pb2 import Repository
from hgitaly import stream
from hgitaly.stub.repository_pb2 import (
    CreateRepositoryRequest,
    CreateBundleRequest,
    CreateBundleFromRefListRequest,
    CreateRepositoryFromBundleRequest,
    FindMergeBaseRequest,
    FullPathRequest,
    RemoveAllRequest,
    RemoveRepositoryRequest,
    SearchFilesByContentRequest,
    SearchFilesByNameRequest,
    SetFullPathRequest,
)
from hgitaly.stub.repository_pb2_grpc import RepositoryServiceStub
from heptapod.testhelpers import (
    LocalRepoWrapper,
    git,
)

from . import skip_comparison_tests
if skip_comparison_tests():  # pragma no cover
    pytestmark = pytest.mark.skip

parametrize = pytest.mark.parametrize

TIP_TAG_NAME = b'tip'


def test_compare_find_merge_base(gitaly_comparison):
    fixture = gitaly_comparison
    gitaly_repo = fixture.gitaly_repo
    git_repo = fixture.git_repo
    wrapper = fixture.hg_repo_wrapper

    # repo structure:
    #
    #   o 3 add animal (branch/stable)
    #   |
    #   | 2 add bar
    #   |/
    #   o 1 add zoo
    #   |
    #   o 0 add foo
    #
    gl_branch = b'branch/default'
    sha0 = wrapper.write_commit('foo').hex()
    git_shas = {
        sha0: git_repo.branches()[gl_branch]['sha']
    }
    ctx1 = wrapper.write_commit('zoo')
    sha1 = ctx1.hex()
    git_shas[sha1] = git_repo.branches()[gl_branch]['sha']
    sha2 = wrapper.write_commit('bar').hex()
    git_shas[sha2] = git_repo.branches()[gl_branch]['sha']
    sha3 = wrapper.write_commit('animal', branch='stable', parent=ctx1).hex()
    git_shas[sha3] = git_repo.branches()[b'branch/stable']['sha']
    # commiting a new root, which will test the case when there
    # is no merge_base (gca)
    sha4 = wrapper.commit_file('tut', branch='other',
                               parent=node_mod.nullid).hex()
    git_shas[sha4] = git_repo.branches()[b'branch/other']['sha']

    diff_stubs = dict(
        git=RepositoryServiceStub(fixture.gitaly_channel),
        hg=RepositoryServiceStub(fixture.hgitaly_channel),
    )

    def do_rpc(vcs, revisions):
        if vcs == 'git':
            revs = [git_shas.get(rev, rev) for rev in revisions]
            revisions = revs

        request = FindMergeBaseRequest(
            repository=gitaly_repo,
            revisions=revisions,
        )

        response = diff_stubs[vcs].FindMergeBase(request)
        base = pycompat.sysbytes(response.base)
        if not base:
            return base
        return base if vcs == 'git' else git_shas[base]

    list_of_interesting_revs = [b'branch/default', b'branch/stable',
                                sha0, sha1, sha4]
    for rev_pair in itertools.product(list_of_interesting_revs, repeat=2):
        assert do_rpc('hg', rev_pair) == do_rpc('git', rev_pair)

    # test with invalid_argument, as it requires minimum 2 revisions
    with pytest.raises(grpc.RpcError) as exc_info_hg:
        do_rpc('hg', [sha0])
    with pytest.raises(grpc.RpcError) as exc_info_git:
        do_rpc('git', [git_shas[sha0]])
    assert exc_info_hg.value.code() == exc_info_git.value.code()
    assert exc_info_hg.value.details() == exc_info_git.value.details()

    sha_not_exists = b'deadnode' * 5
    assert (
        do_rpc('hg', [sha0, sha_not_exists])
        ==
        do_rpc('git', [git_shas[sha0], sha_not_exists])
    )


def test_compare_create_repository(
        gitaly_channel, grpc_channel, server_repos_root):
    rel_path = 'sample_repo'
    default_storage = 'default'
    repo_stubs = dict(
        hg=RepositoryServiceStub(grpc_channel),
        git=RepositoryServiceStub(gitaly_channel)
    )

    def do_rpc(vcs, rel_path, storage=default_storage):
        grpc_repo = Repository(relative_path=rel_path,
                               storage_name=storage)
        request = CreateRepositoryRequest(repository=grpc_repo)
        response = repo_stubs[vcs].CreateRepository(request)
        return response

    hg_rel_path = rel_path + '.hg'
    git_rel_path = rel_path + '.git'
    # actual test
    assert do_rpc('hg', hg_rel_path) == do_rpc('git', git_rel_path)

    # when repo already exists (actually its directory)
    with pytest.raises(grpc.RpcError) as exc_info_git:
        do_rpc('git', git_rel_path)
    with pytest.raises(grpc.RpcError) as exc_info_hg:
        do_rpc('hg', hg_rel_path)
    assert exc_info_hg.value.code() == exc_info_git.value.code()

    # when storage name is invalid
    with pytest.raises(grpc.RpcError) as exc_info_hg:
        do_rpc('hg', rel_path, storage='cargoship')
    with pytest.raises(grpc.RpcError) as exc_info_git:
        do_rpc('git', rel_path, storage='cargoship')
    assert exc_info_hg.value.code() == exc_info_git.value.code()
    assert 'no such storage' in exc_info_hg.value.details()
    assert 'no such storage' in exc_info_git.value.details()

    # test with a broken symlink (which points to itself)
    # it used to be an error for both, with Gitaly complaining
    # that the file exists (but would not raise an error for
    # an existing proper Git repo). As of 14.6, Gitaly refuses
    # all existing files, including broken symlinks
    # As a consequence of the added early check, we don't have
    # any case of `hg init` itself failing on hand.
    repo_name = "myrepo_a_broken_symlink"
    path = (server_repos_root / default_storage / repo_name)
    path.symlink_to(path)
    with pytest.raises(grpc.RpcError) as exc_info_hg:
        do_rpc('hg', repo_name)
    with pytest.raises(grpc.RpcError) as exc_info_git:
        do_rpc('git', repo_name)
    exc_hg, exc_git = exc_info_hg.value, exc_info_git.value
    assert exc_hg.code() == exc_git.code()
    for exc in (exc_hg, exc_git):
        assert 'exists already' in exc.details()


def test_remove_repository(gitaly_comparison, server_repos_root):
    fixture = gitaly_comparison
    grpc_repo = fixture.gitaly_repo
    rpc_helper = fixture.rpc_helper(
        stub_cls=RepositoryServiceStub,
        method_name='RemoveRepository',
        request_cls=RemoveRepositoryRequest,
    )
    assert_compare_errors = rpc_helper.assert_compare_errors

    # unknown storage and missing repo
    assert_compare_errors(same_details=False,
                          repository=Repository(storage_name='unknown',
                                                relative_path='/some/path'))
    assert_compare_errors(
        repository=Repository(storage_name=grpc_repo.storage_name,
                              relative_path='no/such/path'))


@parametrize('hg_server', ('hgitaly', 'rhgitaly'))
def test_repository_exists(gitaly_rhgitaly_comparison,
                           hg_server,
                           server_repos_root):
    fixture = gitaly_rhgitaly_comparison
    grpc_repo = fixture.gitaly_repo
    rpc_helper = fixture.rpc_helper(
        stub_cls=RepositoryServiceStub,
        method_name='RepositoryExists',
        request_cls=RemoveRepositoryRequest,
        hg_server=hg_server,
    )
    assert_compare = rpc_helper.assert_compare
    assert_compare_errors = rpc_helper.assert_compare_errors

    assert_compare(repository=grpc_repo)
    assert_compare(
        repository=Repository(storage_name=grpc_repo.storage_name,
                              relative_path='no/such/path'))

    # missing repo *message* (!)
    assert_compare_errors(repository=None, same_details=False)

    # unknown storage
    assert_compare_errors(same_details=False,
                          repository=Repository(storage_name='unknown',
                                                relative_path='/some/path'))


@parametrize('hg_server', ('hgitaly', 'rhgitaly'))
def test_has_local_branches(gitaly_rhgitaly_comparison,
                            server_repos_root,
                            hg_server):
    fixture = gitaly_rhgitaly_comparison
    grpc_repo = fixture.gitaly_repo
    rpc_helper = fixture.rpc_helper(
        hg_server=hg_server,
        stub_cls=RepositoryServiceStub,
        method_name='HasLocalBranches',
        request_cls=RemoveRepositoryRequest,
    )
    assert_compare = rpc_helper.assert_compare
    assert_compare_errors = rpc_helper.assert_compare_errors

    assert_compare(repository=grpc_repo)

    # repo does not exist
    assert_compare_errors(
        same_details=False,
        repository=Repository(storage_name=grpc_repo.storage_name,
                              relative_path='no/such/path'))

    # missing repo *message* (!)
    assert_compare_errors(repository=None, same_details=False)

    # unknown storage
    assert_compare_errors(same_details=False,
                          repository=Repository(storage_name='unknown',
                                                relative_path='/some/path'))


def test_full_path(gitaly_comparison, server_repos_root):
    fixture = gitaly_comparison
    grpc_repo = fixture.gitaly_repo

    rpc_helper = fixture.rpc_helper(
        stub_cls=RepositoryServiceStub,
        method_name='FullPath',
        request_cls=FullPathRequest,
    )
    assert_compare_errors = rpc_helper.assert_compare_errors

    # path not set on existing repo
    assert_compare_errors(same_details=False)

    # unknown storage and missing repo
    assert_compare_errors(same_details=False,
                          repository=Repository(storage_name='unknown',
                                                relative_path='/some/path'))
    assert_compare_errors(
        same_details=False,
        repository=Repository(storage_name=grpc_repo.storage_name,
                              relative_path='no/such/path'))


def test_set_full_path(gitaly_comparison, server_repos_root):
    fixture = gitaly_comparison

    rpc_helper = fixture.rpc_helper(
        stub_cls=RepositoryServiceStub,
        method_name='SetFullPath',
        request_cls=SetFullPathRequest,
    )
    assert_compare = rpc_helper.assert_compare
    assert_error_compare = rpc_helper.assert_compare_errors

    # success case
    assert_compare(path='group/project')

    # error cases
    assert_error_compare('')

    assert_error_compare(path='some/full/path',
                         repository=Repository(
                             storage_name=fixture.gitaly_repo.storage_name,
                             relative_path='no/such/repo'),
                         same_details=False,
                         )

    assert_error_compare(path='some/full/path',
                         same_details=False,
                         repository=Repository(
                             relative_path=fixture.gitaly_repo.relative_path,
                             storage_name='unknown'))


def assert_compare_hg_git_created_repos(target_hgrepo, target_gitrepo):
    # assert branches
    br_prefix = b'branch/'
    hgbranches = set(
        [br[0] for br in target_hgrepo.branchmap().iterbranches()])
    gitbranches = set(
        [br[len(br_prefix):] for br in target_gitrepo.branches().keys()])
    assert hgbranches == gitbranches

    # assert tags
    hg_tags = set(target_hgrepo.tags().keys())
    hg_tags.remove(TIP_TAG_NAME)
    git_tags = set(target_gitrepo.tags())
    assert hg_tags == git_tags


def test_compare_create_bundle_and_create_repository_from_bundle(
        gitaly_comparison, tmpdir, server_repos_root):
    default_storage = 'default'
    fixture = gitaly_comparison
    gitaly_repo = fixture.gitaly_repo
    wrapper = fixture.hg_repo_wrapper

    # repo structure:
    #
    #   @ 3 zoo (phase: draft) (amended) (branch:feature)
    #   |
    #   | o 1 bar (phase: public) (tag: v1.2.3)
    #   |/
    #   o 0 foo (phase: public)
    #
    ctx0 = wrapper.commit_file('foo')
    sha0 = ctx0.hex()
    sha1 = wrapper.commit_file('bar').hex()
    wrapper.commit_file('zoo', parent=ctx0, branch='feature')
    wrapper.amend_file('zoo')
    wrapper.set_phase('public', [sha0, sha1])
    wrapper.update(sha1)
    wrapper.command('tag', b'v1.2.3', rev=sha1)
    wrapper.command('gitlab-mirror')

    hg_rel_path = 'target_hg_repo'
    git_rel_path = 'target_git_repo'
    hgrepo_fullpath = server_repos_root / default_storage / hg_rel_path
    gitrepo_fullpath = server_repos_root / default_storage / git_rel_path
    target_repo_msg = dict(
        hg=Repository(relative_path=hg_rel_path,
                      storage_name=default_storage),
        git=Repository(relative_path=git_rel_path,
                       storage_name=default_storage))
    bundle_path = dict(
        hg=tmpdir / 'hg.bundle',
        git=tmpdir / 'git.bundle')
    repo_stub = dict(
        hg=RepositoryServiceStub(fixture.hgitaly_channel),
        git=RepositoryServiceStub(fixture.gitaly_channel))

    def rpc_create_bundle(vcs):
        request = CreateBundleRequest(repository=gitaly_repo)
        response = repo_stub[vcs].CreateBundle(request)
        with open(bundle_path[vcs], 'wb') as fobj:
            for chunk in response:
                fobj.write(chunk.data)

    def rpc_create_repository_from_bundle(vcs):
        with open(bundle_path[vcs], 'rb') as fobj:
            data = fobj.read()
            first_req_data_size = len(data) // 2
            request1 = CreateRepositoryFromBundleRequest(
                repository=target_repo_msg[vcs],
                data=data[:first_req_data_size])
            request2 = CreateRepositoryFromBundleRequest(
                data=data[first_req_data_size:])
            # create an iterator of requests
            request = (req for req in [request1, request2])
            return repo_stub[vcs].CreateRepositoryFromBundle(request)

    # Actual test
    rpc_create_bundle('hg')
    rpc_create_bundle('git')
    rpc_create_repository_from_bundle('hg')
    rpc_create_repository_from_bundle('git')

    target_hgrepo = LocalRepoWrapper.load(hgrepo_fullpath).repo
    target_gitrepo = git.GitRepo(gitrepo_fullpath)

    assert_compare_hg_git_created_repos(target_hgrepo, target_gitrepo)

    # test error case: when repo already exists
    with pytest.raises(grpc.RpcError) as exc_info_git:
        rpc_create_repository_from_bundle('git')
    with pytest.raises(grpc.RpcError) as exc_info_hg:
        rpc_create_repository_from_bundle('hg')
    assert exc_info_hg.value.code() == exc_info_git.value.code()
    assert exc_info_hg.value.details() == exc_info_git.value.details()

    # edge case: empty request
    with pytest.raises(grpc.RpcError) as exc_info_git:
        repo_stub['git'].CreateRepositoryFromBundle(())
    with pytest.raises(grpc.RpcError) as exc_info_hg:
        repo_stub['hg'].CreateRepositoryFromBundle(())
    assert exc_info_hg.value.code() == exc_info_git.value.code()
    assert exc_info_hg.value.details() == exc_info_git.value.details()


def test_create_bundle_from_ref_list(
        gitaly_comparison, tmpdir, server_repos_root):
    default_storage = 'default'
    fixture = gitaly_comparison
    gitaly_repo = fixture.gitaly_repo
    wrapper = fixture.hg_repo_wrapper

    # repo structure:
    #
    #   @ 3 zoo (branch:toy) (phase: draft) (amended)
    #   |
    #   | o 1 bar (branch: animal) (tag: v1.2.3)
    #   |/
    #   o 0 foo (branch: default)
    #
    ctx0 = wrapper.commit_file('foo')
    sha0 = ctx0.hex()
    sha1 = wrapper.commit_file('bar', branch='animal').hex()
    wrapper.commit_file('zoo', parent=ctx0, branch='toys').hex()
    wrapper.amend_file('zoo')
    wrapper.set_phase('public', [sha0, sha1])
    wrapper.update(sha1)
    wrapper.command('tag', b'v1.2.3', rev=sha1)
    wrapper.command('gitlab-mirror')

    def target_repo_path(vcs, bundle_name):
        relative_path = '%s_%s_repo' % (vcs, bundle_name)
        return server_repos_root / default_storage / relative_path

    def target_repo_msg(vcs, bundle_name):
        relative_path = '%s_%s_repo' % (vcs, bundle_name)
        # relative_path = vcs + bundle_name
        return Repository(relative_path=relative_path,
                          storage_name=default_storage)

    def target_repo(vcs, bundle_name):
        path = target_repo_path(vcs, bundle_name)
        if vcs == 'git':
            return git.GitRepo(path)
        return LocalRepoWrapper.load(path).repo.unfiltered()

    def vcs_qualified_bundle_path(vcs, bundle_name):
        return tmpdir / (vcs + bundle_name)

    repo_stub = dict(
        hg=RepositoryServiceStub(fixture.hgitaly_channel),
        git=RepositoryServiceStub(fixture.gitaly_channel),
    )

    def rpc_create_bundle_from_ref_list(
            vcs, bundle_name, refs, without_repository=False):
        bundle_path = vcs_qualified_bundle_path(vcs, bundle_name)

        def get_request_iter(refs):
            first_req = True
            for chunk in stream.split_batches(refs, 2):
                if first_req and not without_repository:
                    first_req = False
                    yield CreateBundleFromRefListRequest(
                        repository=gitaly_repo,
                        patterns=chunk)
                    continue
                yield CreateBundleFromRefListRequest(patterns=chunk)

        request = get_request_iter(refs)
        response = repo_stub[vcs].CreateBundleFromRefList(request)
        with open(bundle_path, 'wb') as fobj:
            for chunk in response:
                fobj.write(chunk.data)

    def rpc_create_repository_from_bundle(vcs, bundle_name):
        bundle_path = vcs_qualified_bundle_path(vcs, bundle_name)

        def get_request_iter(data):
            first_req = True
            for chunk in stream.split_batches(data, 10):
                if first_req:
                    first_req = False
                    yield CreateRepositoryFromBundleRequest(
                        repository=target_repo_msg(vcs, bundle_name),
                        data=chunk)
                    continue
                yield CreateRepositoryFromBundleRequest(data=chunk)

        with open(bundle_path, 'rb') as fobj:
            data = fobj.read()
            request = get_request_iter(data)
            return repo_stub[vcs].CreateRepositoryFromBundle(request)

    def create_bundle(bundle_name, *refs):
        rpc_create_bundle_from_ref_list('hg', bundle_name, refs)
        rpc_create_bundle_from_ref_list('git', bundle_name, refs)

    def create_repository_from_bundle(bundle_name):
        rpc_create_repository_from_bundle('hg', bundle_name)
        rpc_create_repository_from_bundle('git', bundle_name)

    def assert_compare_created_repository_from_bundle(bundle_name):
        target_hgrepo = target_repo('hg', bundle_name)
        target_gitrepo = target_repo('git', bundle_name)
        assert_compare_hg_git_created_repos(target_hgrepo, target_gitrepo)

    # 1) test with all refs
    allrefs_bundle = 'all_refs_bundle'
    create_bundle(
        allrefs_bundle,
        b'refs/heads/branch/animal', b'refs/heads/branch/toys',
        b'refs/heads/branch/default', b'refs/tags/v1.2.3')
    create_repository_from_bundle(allrefs_bundle)
    # test successful repo creation from bundle
    assert_compare_created_repository_from_bundle(allrefs_bundle)

    # 2) test with some refs
    somerefs_bundle = 'some_refs_bundle'
    create_bundle(
        somerefs_bundle,
        b'refs/heads/branch/default', b'refs/heads/branch/toys')
    create_repository_from_bundle(somerefs_bundle)
    # test successful repo creation from bundle
    assert_compare_created_repository_from_bundle(somerefs_bundle)

    # test error case: no repository object in request
    with pytest.raises(grpc.RpcError) as exc_info_git:
        rpc_create_bundle_from_ref_list(
            'git', 'temp_bname', [b'refs/heads/branch/default'],
            without_repository=True)
    with pytest.raises(grpc.RpcError) as exc_info_hg:
        rpc_create_bundle_from_ref_list(
            'hg', 'temp_bname', [b'refs/heads/branch/default'],
            without_repository=True)
    assert exc_info_hg.value.code() == exc_info_git.value.code()
    assert exc_info_hg.value.details() == exc_info_git.value.details()

    # test error case: error in bundle application

    (tmpdir / 'hgbroken-bundle').write("Obviously garbage")
    (tmpdir / 'gitbroken-bundle').write("Garbage, yes, but Git garbage!")
    with pytest.raises(grpc.RpcError) as exc_info_hg:
        rpc_create_repository_from_bundle('hg', 'broken-bundle')
    with pytest.raises(grpc.RpcError) as exc_info_git:
        rpc_create_repository_from_bundle('git', 'broken-bundle')
    assert exc_info_hg.value.code() == exc_info_git.value.code()

    for vcs in ('hg', 'git'):
        assert not target_repo_path(vcs, 'broken-bundle').exists()


def test_search_files_by_name(gitaly_comparison):
    fixture = gitaly_comparison

    wrapper = fixture.hg_repo_wrapper
    ctx0 = wrapper.write_commit('afoo', message="Some foo")
    sub = (wrapper.path / 'sub')
    sub.mkdir()
    (sub / 'bar').write_text('bar content')
    (sub / 'ba2').write_text('ba2 content')
    # TODO OS indep for paths (actually TODO make wrapper.commit easier to
    # use, e.g., check how to make it accept patterns)
    wrapper.commit(rel_paths=['sub/bar', 'sub/ba2'],
                   message="zebar", add_remove=True)

    wrapper.write_commit('animals', message="A branch without subdir",
                         branch='other', parent=ctx0)

    default_rev = b'branch/default'

    rpc_helper = fixture.rpc_helper(stub_cls=RepositoryServiceStub,
                                    method_name='SearchFilesByName',
                                    request_cls=SearchFilesByNameRequest,
                                    request_defaults=dict(
                                        ref=default_rev,
                                        limit=0,
                                        offset=0),
                                    streaming=True,
                                    )
    assert_compare = rpc_helper.assert_compare
    assert_compare_errors = rpc_helper.assert_compare_errors

    # precondition for the test: mirror worked
    assert fixture.git_repo.branch_titles() == {
        default_rev: b"zebar",
        b'branch/other': b"A branch without subdir",
    }

    assert_compare(filter='/bar', query='.')
    assert_compare(filter='^sub/', query='.')
    assert_compare(filter='a', query='sub')
    assert_compare(filter='b?r$', query='sub')

    # without filter
    assert_compare(query='.')
    assert_compare(query='sub')

    # offset and limit (we have 3 matches without filter)
    assert_compare(query='.', limit=2)
    assert_compare(query='.', limit=1, offset=1)  # both sort lexicographically

    # from a different ref
    assert_compare(filter='bar', query='.', ref=b'branch/other')  # no match
    assert_compare(filter='.*', query='.', ref=b'branch/other')

    # query is mandatory
    assert_compare_errors(filter='/ba')

    # problems with regexp
    assert_compare_errors(filter='\\', query='.', same_details=False)
    assert_compare_errors(filter='a' * 1001, query='.')

    # unknown ref gives back an empty list of files, not an error
    assert_compare(ref=b'unknown', query='.')


def test_search_files_by_content(gitaly_comparison):
    fixture = gitaly_comparison

    wrapper = fixture.hg_repo_wrapper
    wrapper.write_commit('afoo', message="Some foo")
    sub = (wrapper.path / 'sub')
    sub.mkdir()
    (sub / 'bar').write_text('line1\nline2\nbar content\nline4\nline5')
    (sub / 'ba2').write_text('line1\nba2 content')
    (sub / 'ba3').write_text('ba3 content\nline2')
    # This one has a Windows endings, and exhibits that `git grep` normalizes
    # to `\n`. Also Git does not interpret the MacOS classic line ending
    # '\r' and we do. In that case, we can claim our response to be more
    # correct and we will not compare it.
    (sub / 'ba4').write_text('l1\r\nl2\nl3\nba4 content\nline6')
    (sub / 'ba5').write_text('m1\nm2\nm3\nm4\nm5\nm6\nba5 content\n')
    (wrapper.path / 'large').write_text('very large content\n' * 3000)
    # TODO OS indep for paths (actually TODO make wrapper.commit easier to
    # use, e.g., check how to make it accept patterns)
    wrapper.commit(rel_paths=['sub/bar', 'sub/ba2', 'sub/ba3',
                              'sub/ba4', 'sub/ba5', 'large'],
                   message="zebar", add_remove=True)

    default_rev = b'branch/default'

    rpc_helper = fixture.rpc_helper(
        stub_cls=RepositoryServiceStub,
        method_name='SearchFilesByContent',
        request_cls=SearchFilesByContentRequest,
        request_defaults=dict(
            ref=default_rev,
        ),
        streaming=True,
        error_details_normalizer=lambda s, vcs: s.lower(),
    )
    assert_compare = rpc_helper.assert_compare
    assert_compare_errors = rpc_helper.assert_compare_errors

    # precondition for the test: mirror worked
    assert fixture.git_repo.branch_titles() == {
        default_rev: b"zebar",
    }
    assert_compare(query='no match for this one')
    assert_compare(query='^bar.c')
    assert_compare(query='^ba2.c')   # only one line before match
    assert_compare(query='^ba3.c')   # only one line after match
    assert_compare(query='^ba4.c')   # more than two lines before match
    assert_compare(query='^very')
    assert_compare(query='^l1|ba4')  # two matches with overlapping context
    assert_compare(query='^m1|ba5')  # two matches with non-overlapping context
    assert_compare(query='ConTent')  # several files and case insensity

    # errors if query is missing
    assert_compare_errors()
    assert_compare_errors(ref=b'topic/default/does-not-exist')
    # unresolvable ref
    assert_compare(ref=b'topic/default/does-not-exist', query='foo')
    # missing repo, ref
    assert_compare_errors(ref=b'')
    assert_compare_errors(repository=None)
    fixture.gitaly_repo.relative_path = 'no/such/repo'
    assert_compare_errors(query='foo', same_details=False)


def test_remove_all(gitaly_comparison, server_repos_root):
    fixture = gitaly_comparison
    rpc_helper = fixture.rpc_helper(
        stub_cls=RepositoryServiceStub,
        method_name='RemoveAll',
        request_cls=RemoveAllRequest,
        repository_arg=False,
    )
    assert_compare_errors = rpc_helper.assert_compare_errors

    # unknown storage
    assert_compare_errors(storage_name='unknown')
