# Copyright 2023 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
from multiprocessing import Process, Pipe
import shutil
import signal

import warnings

from mercurial import error
from hgext3rd.heptapod.branch import set_default_gitlab_branch

import pytest
from pytest_cov.embed import cleanup_on_signal

from heptapod.testhelpers import (
    LocalRepoWrapper,
)

from ..workdir import (
    ROSTER_FILE_NAME,
    locked_roster,
    roster_iter,
    wd_path,
    release_workdir,
    reserve_workdir,
    working_directory,
    workdirs_gc,
)

parametrize = pytest.mark.parametrize


@pytest.fixture
def wd_fixture(tmpdir):
    """Shared fixture for working directories tests

    the first object is the `Path` to the working directories root.
    The second object is the wrapper for a freshly created, empty,
    repository.
    """
    workdirs_root = tmpdir / 'working-directories'
    wrapper = LocalRepoWrapper.init(tmpdir / 'repo',
                                    config=dict(
                                     extensions=dict(topic='', evolve=''),
                                    ))
    yield workdirs_root, wrapper


def test_working_directory_basic(wd_fixture):
    wds_root, wrapper = wd_fixture
    src_repo = wrapper.repo

    with working_directory(wds_root, src_repo) as wd:
        wd_path = wd.path
        wd_id = wd.id
        # caller would typically use `wd.repo`, yet not necessarily
        wd_wrapper = LocalRepoWrapper.load(wd.path)
        sha = wd_wrapper.commit_file('foo').hex()

    # The commit done in the temporary working directory is visbile from
    # the main repository.
    wrapper.reload()

    ctx = src_repo[sha]
    assert ctx.hex() == sha

    # Simple reuse, with an error in usage
    try:
        with working_directory(wds_root, src_repo) as wd:
            assert wd.path == wd_path
            raised = RuntimeError("Workdir tests error")
            raise raised
    except RuntimeError as caught:
        assert caught is raised

    # The working dir has been released despite of the RuntimeError,
    # we can use it again
    with working_directory(wds_root, src_repo, changeset=ctx) as wd:
        assert wd.path == wd_path
        wd_wrapper = LocalRepoWrapper.load(wd.path)
        assert wd_wrapper.repo[sha].branch() == b'default'

    # Two working directories for the same branch
    with working_directory(wds_root, src_repo, changeset=ctx) as wd1:
        with working_directory(wds_root, src_repo, changeset=ctx) as wd2:
            assert wd1.path == wd_path
            assert wd2.path != wd_path
            wd2_path = wd2.path
            wd2_id = wd2.id

    # We now have two available working directories for the default branch
    with src_repo.vfs(ROSTER_FILE_NAME, b'rb') as rosterf:
        wds = {wd_id: branch
               for (wd_id, _, _, branch), _l in roster_iter(rosterf)}
    assert wds == {wd_id: b'default', wd2_id: b'default'}

    # Both can be reused
    with working_directory(wds_root, src_repo, changeset=ctx) as wd1:
        with working_directory(wds_root, src_repo, changeset=ctx) as wd2:
            assert set((wd1.path, wd2.path)) == {wd_path, wd2_path}


def test_working_directory_branches(wd_fixture):
    wds_root, wrapper = wd_fixture
    src_repo = wrapper.repo

    cs_default = wrapper.commit_file('foo')
    cs_topic = wrapper.commit_file('bar', content="top bar", topic='zetop')
    cs_other = wrapper.commit_file('branch', branch='other', parent=cs_default)

    with working_directory(wds_root, wrapper.repo, changeset=cs_topic) as wd:
        default_wd_id = wd.id

        wctx = wd.repo[None]
        assert wctx.p1() == cs_topic
        assert wctx.branch() == b'default'
        assert wctx.topic() == b'zetop'

        assert (wd.path / 'foo').exists()
        assert (wd.path / 'bar').exists()

    with working_directory(wds_root, wrapper.repo, changeset=cs_other) as wd:
        assert wd.id != default_wd_id
        other_wd_id = wd.id

        wctx = wd.repo[None]
        assert wctx.p1() == cs_other
        assert wctx.branch() == b'other'
        assert not wctx.topic()

        assert (wd.path / 'foo').exists()
        assert (wd.path / 'branch').exists()
        assert not (wd.path / 'bar').exists()

        other_wd_path = wd.path

    with src_repo.vfs(ROSTER_FILE_NAME, b'rb') as rosterf:
        wds = {wd_id: branch
               for (wd_id, _, _, branch), _l in roster_iter(rosterf)}

    assert wds == {default_wd_id: b'default', other_wd_id: b'other'}

    # If the working directory is missing despite being listed, it is not
    # an issue. Could happen with restore from backup (although we should
    # simply not backup the roster file) or be accidental.
    shutil.rmtree(other_wd_path)
    assert not other_wd_path.exists()

    with working_directory(wds_root, wrapper.repo, changeset=cs_other) as wd:
        assert wd.id == other_wd_id
        assert wd.path == other_wd_path

    # Working directories are reused regardless of topic
    with working_directory(wds_root, wrapper.repo, changeset=cs_default) as wd:
        assert wd.id == default_wd_id

        wctx = wd.repo[None]
        assert wctx.p1() == cs_default
        assert wctx.branch() == b'default'
        assert not wctx.topic()

        # testing purge/clean update
        (wd.path / 'bar').write_bytes(b"Some conflicting unversioned content")

    # Even with conflicting unversioned file, a clean working directory is
    # provided on next usage
    with working_directory(wds_root, wrapper.repo, changeset=cs_topic) as wd:
        assert wd.id == default_wd_id

        wctx = wd.repo[None]
        assert wctx.p1() == cs_topic

        assert (wd.path / 'bar').read_bytes() == b"top bar"

        # Acquire Mercurial's wlock, but doesn't release it, as would happen
        # on SIGKILL. It is essential for the test to be meaningful to keep
        # a reference to the lock.
        wlock = wd.repo.wlock()

    # Working directory locks are broken on entering if needed.
    # This would block otherwise, due to the update to the given changeset:
    with working_directory(wds_root, wrapper.repo, changeset=cs_default) as wd:
        assert wd.id == default_wd_id

    # Ironically, there's a warning to use `wlock.release` instead of `del`
    # to release a lock, which is not exactly why we delete it (mostly keeping
    # flake8 happy with this test code).
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=DeprecationWarning)
        del wlock

    # working directories on obsolete changesets are legitimate
    wrapper.update_bin(cs_topic.node())
    wrapper.amend_file('bar', content="new_bar")

    with working_directory(wds_root, wrapper.repo, changeset=cs_topic) as wd:
        assert wd.id == default_wd_id

        wctx = wd.repo[None]
        parent_cs = wctx.p1()
        assert parent_cs == cs_topic
        assert parent_cs.obsolete()


@pytest.fixture
def purge_fixture(wd_fixture):
    wds_root, wrapper = wd_fixture
    repo = wrapper.repo
    # using a custom default branch to illustrate that 'default' is not
    # hardcoded
    wrapper.commit_file('foo', branch='mydefault')
    set_default_gitlab_branch(repo, b'branch/mydefault')

    return wd_fixture


def test_workdirs_gc_active_default(purge_fixture):
    wds_root, wrapper = purge_fixture
    repo = wrapper.repo

    # no error if there is no working directory
    workdirs_gc(wds_root, repo, 1)

    wd_path(wds_root, 1).mkdir(parents=True)
    wd_path(wds_root, 2).mkdir()
    with locked_roster(repo) as (inf, outf):
        outf.writelines((b"0 12 10000 mydefault\n",
                         b"1 - 10000 other\n",
                         b"2 - 10000 mydefault\n",
                         ))

    workdirs_gc(wds_root, repo, max_age_seconds=100, now=11000)

    # The active work dir for default branch is kept, considered to be enough
    with locked_roster(repo) as (inf, outf):
        lines = inf.readlines()
        assert lines == [b"0 12 10000 mydefault\n"]


def test_workdirs_gc_stale_default(purge_fixture):
    wds_root, wrapper = purge_fixture
    repo = wrapper.repo

    # no error if there is no working directory
    workdirs_gc(wds_root, repo, 1)

    wd_path(wds_root, 0).mkdir(parents=True)
    wd_path(wds_root, 2).mkdir()
    with locked_roster(repo) as (inf, outf):
        outf.writelines((b"0 - 10000 mydefault\n",
                         b"2 - 15000 mydefault\n",
                         ))

    workdirs_gc(wds_root, repo, max_age_seconds=100, now=20000)

    # The active work dir for default branch is kept, considered to be enough
    with locked_roster(repo) as (inf, outf):
        lines = [parsed for parsed, _line in roster_iter(inf)]
        assert len(lines) == 1
        assert lines[0][3] == b'mydefault'


def test_workdirs_gc_no_default(purge_fixture):
    wds_root, wrapper = purge_fixture
    repo = wrapper.repo

    # no error if there is no working directory
    workdirs_gc(wds_root, repo, 1)

    wd_path(wds_root, 0).mkdir(parents=True)
    wd_path(wds_root, 1).mkdir()
    with locked_roster(repo) as (inf, outf):
        outf.writelines((b"0 - 10000 other\n",
                         b"1 - 15000 another\n",
                         ))

    workdirs_gc(wds_root, repo, max_age_seconds=100, now=20000)

    # The active work dir for default branch is kept, considered to be enough
    with locked_roster(repo) as (inf, outf):
        assert len(inf.read()) == 0


def test_workdirs_gc_rmerror(purge_fixture):
    wds_root, wrapper = purge_fixture
    repo = wrapper.repo

    # no error if there is no working directory
    workdirs_gc(wds_root, repo, 1)

    with locked_roster(repo) as (inf, outf):
        outf.writelines((b"0 - 10000 other\n",
                         b"1 - 15000 mydefault\n",
                         ))

    workdirs_gc(wds_root, repo, max_age_seconds=100, now=20000)

    with locked_roster(repo) as (inf, outf):
        wds = {parsed[0]: parsed[3] for parsed, _line in roster_iter(inf)}
        assert wds == {0: b'other', 1: b'mydefault'}


def assert_recv(pipe, expected, timeout=2):
    """Read data from a pipe and assert it is as expected, without blocking.

    Using this rather than just `pipe.recv()` prevents blocking the
    tests upon errors.

    The default timeout is long, but acceptable to humans and CI jobs.
    """
    assert pipe.poll(timeout=timeout)
    assert pipe.recv() == expected


ROSTER_LOCK_TIMEOUT = 0.1
ROSTER_LOCK_ATTEMPTS_DELAY = ROSTER_LOCK_TIMEOUT / 10


def locking_subpro(repo_path, conn):
    """Subprocess taking the roster lock and then taking commands from a pipe.

    The lock is taken at startup after sending the initial message and
    is held until the 'shutdown' message is received
    """
    cleanup_on_signal(signal.SIGTERM)
    cleanup_on_signal(signal.SIGINT)
    from hgitaly import procutil
    procutil.IS_CHILD_PROCESS = True

    repo = LocalRepoWrapper.load(repo_path).repo
    conn.send('started')
    try:
        with locked_roster(repo, timeout=ROSTER_LOCK_TIMEOUT) as (inf, outf):
            conn.send('locked')
            while True:
                msg = conn.recv()
                if msg == 'shutdown':
                    conn.send('bye')
                    conn.close()
                    return
                if isinstance(msg, tuple) and msg[0] == 'write':
                    outf.write(msg[1].encode('utf8'))
                    # atomictempfile does not implement flush
                    conn.send('written')
                if msg == 'read':
                    if inf is None:
                        conn.send(None)
                    else:
                        pos = inf.tell()
                        inf.seek(0)
                        conn.send(inf.read().decode('utf8'))
                        inf.seek(pos)
    except error.LockHeld:
        conn.send('timeout')


@parametrize('lock_attempts', (1, 4))
def test_locked_roster(wd_fixture, lock_attempts):
    wrapper = wd_fixture[1]
    repo_path = wrapper.path

    pipe1, child_pipe1 = Pipe()
    pipe2, child_pipe2 = Pipe()
    pipe3, child_pipe3 = Pipe()
    pipe4, child_pipe4 = Pipe()
    proc1 = Process(target=locking_subpro, args=(repo_path, child_pipe1))
    proc2 = Process(target=locking_subpro, args=(repo_path, child_pipe2))
    proc3 = Process(target=locking_subpro, args=(repo_path, child_pipe3))
    proc4 = Process(target=locking_subpro, args=(repo_path, child_pipe4))
    procs = [proc1, proc2, proc3, proc4]

    try:
        # proc1 starts, write a line, but does not see it in its input file
        # (atomicity)
        proc1.start()
        assert_recv(pipe1, 'started')
        assert_recv(pipe1, 'locked')
        pipe1.send(('write', 'content1'))
        assert_recv(pipe1, 'written')
        pipe1.send('read')
        assert_recv(pipe1, None)

        # proc2 starts but cannot acquire the lock yet
        proc2.start()
        assert_recv(pipe2, 'started')
        assert not pipe2.poll(
            timeout=ROSTER_LOCK_ATTEMPTS_DELAY * lock_attempts)

        # shutting down proc1
        pipe1.send('shutdown')
        assert_recv(pipe1, 'bye')
        proc1.join()

        # now that proc1 has released the lock, proc2 acquires it and sees the
        # write done by proc1
        assert_recv(pipe2, 'locked')
        pipe2.send('read')
        assert_recv(pipe2, 'content1')

        # proc2 overwrites the file, but does not see the change yet in its
        # input stream
        pipe2.send(('write', 'content2'))
        assert_recv(pipe2, 'written')
        pipe2.send('read')
        assert_recv(pipe2, 'content1')

        # proc3 starts, cannot acquire the lock immediately either
        proc3.start()
        assert_recv(pipe3, 'started')
        assert not pipe3.poll(timeout=ROSTER_LOCK_ATTEMPTS_DELAY)

        # after proc2 shutdown, proc3 sees the new content
        pipe2.send('shutdown')
        assert_recv(pipe2, 'bye')
        proc2.join()
        assert_recv(pipe3, 'locked')
        pipe3.send('read')
        assert_recv(pipe3, 'content2')

        # proc4 starts but proc3 does not release the lock in time
        proc4.start()
        assert_recv(pipe4, 'started')
        assert_recv(pipe4, 'timeout')

        pipe3.send('shutdown')
        assert_recv(pipe3, 'bye')
    finally:
        # avoid blocking the test run if there are errors
        for proc in procs:
            if proc.is_alive():
                proc.terminate()
                proc.join()


def test_roster_lock_breaking(wd_fixture):
    wrapper = wd_fixture[1]
    repo_path = wrapper.path

    pipe1, child_pipe1 = Pipe()
    pipe2, child_pipe2 = Pipe()
    proc1 = Process(target=locking_subpro, args=(repo_path, child_pipe1))
    proc2 = Process(target=locking_subpro, args=(repo_path, child_pipe2))
    procs = [proc1, proc2]

    # let's grab the lock from the main tests process, which is not allowed
    # to take it, as it is not one of the HGitaly worker processes. This
    # simulates the case where the PID has been reused: there *is* a process
    # with that pid.
    try:
        with locked_roster(wrapper.repo) as (inf, outf):
            # proc1 takes the lock, ignoring the lock held with an invalid PID
            proc1.start()
            assert_recv(pipe1, 'started')
            assert_recv(pipe1, 'locked')
            pipe1.send(('write', 'content1'))
            assert_recv(pipe1, 'written')

            # of course the lock taken by proc1 blocks proc2
            # Note that exiting normally the `locked_roster` context manager
            # of the main process would release the lock, even if held by
            # proc1, which looks bad, but is irrelevant: in actual operation,
            # roster locks have to be broken if the holding process have died
            # abruptly enough not to have been able to release the lock.
            proc2.start()
            assert_recv(pipe2, 'started')
            assert not pipe2.poll(timeout=ROSTER_LOCK_ATTEMPTS_DELAY)

            # shutting down proc1
            pipe1.send('shutdown')
            assert_recv(pipe1, 'bye')
            proc1.join()

            # now that proc1 has released the lock, proc2 acquires it
            # and sees the write done by proc1
            assert_recv(pipe2, 'locked')
            pipe2.send('read')
            assert_recv(pipe2, 'content1')
    finally:
        # avoid blocking the test run if there are errors
        for proc in procs:
            if proc.is_alive():
                proc.terminate()
                proc.join()


def reserving_subpro(wds_root, repo_path, conn):
    cleanup_on_signal(signal.SIGTERM)
    cleanup_on_signal(signal.SIGINT)
    repo = LocalRepoWrapper.load(repo_path).repo
    from hgitaly import procutil
    conn.send('started')

    while True:
        msg = conn.recv()
        if msg == 'shutdown':
            conn.send('bye')
            conn.close()
            return

        if msg == 'attach':
            procutil.IS_CHILD_PROCESS = True
            conn.send('service-child')
        if msg == 'detach':
            procutil.IS_CHILD_PROCESS = False
            conn.send('mono-process')
        if msg == 'reserve':
            wd = reserve_workdir(wds_root, repo.ui, repo, b'default')
            conn.send(wd.id)
        if msg == 'release':
            release_workdir(repo, wd)
            conn.send('released')


def test_release_workdir_unknown_process(wd_fixture):
    """Reservations by unknown processes have to be ignored."""
    wds_root, wrapper = wd_fixture
    repo_path = wrapper.path

    pipe1, child_pipe1 = Pipe()
    pipe2, child_pipe2 = Pipe()
    pipe3, child_pipe3 = Pipe()

    proc1 = Process(target=reserving_subpro,
                    args=(wds_root, repo_path, child_pipe1))
    proc2 = Process(target=reserving_subpro,
                    args=(wds_root, repo_path, child_pipe2))
    proc3 = Process(target=reserving_subpro,
                    args=(wds_root, repo_path, child_pipe3))
    procs = [proc1, proc2, proc3]
    try:
        # 1st scenario: working directory reserved with a non-existing PID
        #
        # proc1 makes a wd, then dies before it could release it
        # proc2 detects that proc1 is no longer valid, and reuses the wd as
        # if nothing happened. It is likely that the pid has not been reused
        # yet, though we will need to add an inner test to ensure coverage
        # and avoid flakiness
        proc1.start()
        assert_recv(pipe1, 'started')
        pipe1.send('attach')
        assert_recv(pipe1, 'service-child')
        pipe1.send('reserve')
        assert pipe1.poll(timeout=2)
        wd_id = pipe1.recv()
        # shutdown message would *currently* be enough to get the wished stale
        # workdir, but killing the subprocess makes sure the test will
        # not become tautological if there are changes later on
        proc1.kill()
        proc1.join()

        proc2.start()
        assert_recv(pipe2, 'started')
        pipe2.send('attach')
        assert_recv(pipe2, 'service-child')
        pipe2.send('reserve')
        assert_recv(pipe2, wd_id)
        pipe2.send('release')
        pipe2.send('shutdown')
        proc2.join()

        # 2nd scenario: working directory reserved, PID matches an invalid
        # process (it's been reused since then, perhaps even reboot). We
        # use the main tests process PID as a guaranteed existing yet invalid
        # one (with the current logic). PID 1 would be another possible
        # choice if validity rules change.
        repo = wrapper.repo
        wd = reserve_workdir(wds_root, repo.ui, repo, b'default')
        proc3.start()
        assert_recv(pipe3, 'started')
        pipe3.send('attach')
        assert_recv(pipe3, 'service-child')
        pipe3.send('reserve')
        assert_recv(pipe3, wd.id)
        pipe3.send('release')
    finally:
        # avoid blocking the test run if there are errors
        for proc in procs:
            if proc.is_alive():
                proc.terminate()
                proc.join()
