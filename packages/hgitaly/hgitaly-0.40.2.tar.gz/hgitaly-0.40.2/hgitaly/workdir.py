# Copyright 2023 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
from contextlib import contextmanager
import attr
import errno
import logging
import os
from pathlib import Path
import shutil
import time
from typing import Any
import weakref

from mercurial import (
    cmdutil,
    commands,
    error,
    hg,
    lock,
)
from mercurial.repoview import _filteredrepotypes

from .procutil import is_current_service_process
from .revision import gitlab_revision_changeset

logger = logging.getLogger(__name__)

ROSTER_FILE_NAME = b'hgitaly-working-dirs'
ROSTER_LOCK_NAME = ROSTER_FILE_NAME + b'.lock'


def clear_repo_class(repo_class):
    _filteredrepotypes.pop(repo_class, None)


def wd_path(per_repo_root, wd_id):
    return Path(f'{per_repo_root}/{wd_id}')


@attr.define
class WorkingDirectory:
    """Represents a semi-permanent working directory."""
    id: int
    branch: bytes
    path: Path
    repo: Any = attr.field(repr=False, default=None)

    def roster_line(self, pid=None, timestamp=None):
        """Return a line suitable to put in the roster file.

        :param pid: use ``None`` to give back the working directory to the
          pool, current process id to reserve it.
        :return: bytes, since this is to write in files managed by Mercurial's
         vfs, with end of line included, suitable for use in ``writelines``
         and ``write`` methods.
        """
        if timestamp is None:
            timestamp = int(time.time())

        pid_bytes = b'-' if pid is None else str(pid).encode('ascii')
        return (b'%d %s %d %s\n' % (self.id, pid_bytes,
                                    timestamp, self.branch))

    def load_or_create(self, ui, src_repo):
        path_bytes = bytes(self.path)
        if self.path.exists():
            self.init_repo(hg.repository(ui, path_bytes))
        else:
            self.init_repo(hg.share(ui, src_repo.root, path_bytes,
                                    update=False))

    def command(self, name, *args, hidden=False, **kwargs):
        cmd = cmdutil.findcmd(b'update', commands.table)[1][0]
        repo = self.repo
        if hidden:
            repo = repo.unfiltered()
        return cmd(repo.ui, repo, *args, **kwargs)

    def clean_update(self, target_rev):
        self.command(b'update', target_rev, clean=True, hidden=True)

    def purge(self):
        self.command(b'purge', all=True)

    def init_repo(self, repo):
        weakref.finalize(repo, clear_repo_class, repo.unfiltered().__class__)
        self.repo = repo
        # any existing wlock is lingering, since the whole point of
        # this module is to provide a higher level locking system
        repo.vfs.tryunlink(b'wlock')


@contextmanager
def working_directory(workdirs_root, repo, changeset=None):
    """Context manager for temporary working directories

    Entering this context manager, (typically with the ``with`` statement
    yields a clean working directory for the given repository, cleanly updated
    at the specified changeset.

    The working directory is represented by a :class:`WorkingDirectory`
    instance and is guaranteed to be for exclusive use by the caller.
    It is relturned to the underlying pool when exiting the context.

    The changeset Mercurial branch is used as a heuristic for reuse: it
    is assumed that a working directory previously updated to a changeset
    with the same branch can be quickly updated to the given one.

    The given changeset can be obsolete, allowing to revive it with more than
    a simple `hg touch` equivalent. It is therefore up to the caller to
    check for obsolescence if undesireable (e.g., in mergeability checks).

    :param workdirs_root: path to the directory where working directories
      for the given repo are kept.
    :param repo: Mercurial repository object
    :param changeset: a :class:`changectx` instance. Use `None` to get an
      empty working directory. It will in this case be considered to be for
      the ``default`` branch. This should be used only in the case of
      empty repositories.
    """
    branch = b'default' if changeset is None else changeset.branch()
    wd = reserve_workdir(workdirs_root, repo.ui, repo, branch)
    wd.load_or_create(repo.ui, repo)
    wd.purge()
    if changeset is not None:
        wd.clean_update(changeset.hex())

    try:
        yield wd
    finally:
        release_workdir(repo, wd)


class rosterlock(lock.lock):

    def _lockshouldbebroken(self, locker):
        pid = int(locker.split(b":", 1)[-1].decode('ascii').strip())
        return not is_current_service_process(pid)


def trylock(ui, vfs, lockname, timeout, warntimeout, *args, step=0.1,
            **kwargs):
    """return an acquired lock or raise an a LockHeld exception

    This function is responsible to issue logs about
    the held lock while trying to acquires it.

    Derived from Mercurial's `lock.trylock`, with these differences:

    - using :data:`logger`
    - using :class:`rosterlock`
    - configurable sleep interval (param ``step``), both because roster
      file operations are designed to be fast, and to reach the warntimeout
      in tests without overlong sleeps.
    - timeouts always exist, since server operation must not be stalled
      forever.
    - `acquirefn` is ignored, as we don't need it for the roster lock.
    """

    def log(level, locker):
        """log the "waiting on lock" message through at the given level"""
        pid = locker.split(b":", 1)[-1].decode('ascii')
        logger.log(level, "waiting for lock on %r held by process %r",
                   lk.desc, pid)

    lk = rosterlock(vfs, lockname, 0, *args, dolock=False, **kwargs)

    debugidx = 0
    warningidx = int(warntimeout / step)

    delay = 0
    while True:
        try:
            lk._trylock()
            break
        except error.LockHeld as inst:
            if delay == debugidx:
                log(logging.DEBUG, inst.locker)
            if delay == warningidx:
                log(logging.WARNING, inst.locker)
            if timeout <= delay * step:
                raise error.LockHeld(
                    errno.ETIMEDOUT, inst.filename, lk.desc, inst.locker
                )
            time.sleep(step)
            delay += 1

    lk.delay = delay
    if delay:
        if 0 <= warningidx <= delay:
            logger.warning("got lock after %.2f seconds", delay * step)
        else:
            logger.debug("got lock after %.2f seconds", delay * step)

    return lk


@contextmanager
def locked_roster(repo, timeout=1):
    """Locked read/write access to the repo working directories roster file.

    This context manager provides a pair of open files.
    The first is to be used to read the roster, the second to write it,
    with atomic update occurring at the end of the context.

    The lock is not reentrant, which is good enough for this simple need of
    a very short-lived lock protecting both readind and writing.

    :param timeout: maximum time to wait until the roster lock is acquired.
      The default value is intended for production, tests will set it to
      shorter values.
    """
    vfs = repo.vfs
    # TODO Mercurial lock system does not allow to customize its breaking
    # logic, which is actually causing deadlocks in containers.
    # In HGitaly, we can have much more certainty because of the general
    # prerequisites that a HGitaly service (typically several processes)
    # has exclusive access to this resource.
    # This is more general than the working directories roster lock, but
    # it is dubious that HGitaly ever gets exclusive access to Mercurial
    # content (HTTP pushes could be handled if HGitaly eventually manages
    # the hgwebdir services, but SSH pushes would not).
    ui = repo.ui
    warntimeout = 3 * timeout / 10
    # internal config: ui.signal-safe-lock
    signalsafe = ui.configbool(b'ui', b'signal-safe-lock')

    with trylock(ui, vfs,
                 lockname=ROSTER_LOCK_NAME,
                 timeout=timeout,
                 warntimeout=warntimeout,
                 releasefn=None,
                 acquirefn=None,
                 desc=b'Working directories roster file for %s' % repo.root,
                 signalsafe=signalsafe,
                 step=timeout / 10,
                 ):
        try:
            inf = vfs(ROSTER_FILE_NAME, b'rb')
        except FileNotFoundError:
            inf = None

        with vfs(ROSTER_FILE_NAME, b'wb', atomictemp=True) as outf:
            try:
                yield inf, outf
            finally:
                if inf is not None:
                    inf.close()


def roster_iter(fobj):
    if fobj is None:
        return

    for line in fobj:
        # id, pid, branch  TODO what to do in case of invalid data?
        wd_id, pid, timestamp, wd_branch = line.split(b' ', 3)
        pid = int(pid) if pid != b'-' else None
        yield (int(wd_id), pid, int(timestamp), wd_branch.strip()), line


def roster_branch_match(fobj, branch):
    matching = None
    max_id = - 1
    lines = []
    for (wd_id, pid, _ts, wd_branch), line in roster_iter(fobj):
        if wd_id > max_id:
            max_id = wd_id
        if wd_branch == branch:
            if pid is None or not is_current_service_process(pid):
                matching = wd_id
                continue
        lines.append(line)
    return matching, max_id + 1, lines


def reserve_workdir(workdirs_root, ui, repo, branch):
    current_pid = os.getpid()
    with locked_roster(repo) as (rosterf, new_rosterf):
        matching_id, unused_id, other_lines = roster_branch_match(rosterf,
                                                                  branch)
        wd_id = unused_id if matching_id is None else matching_id
        wd = WorkingDirectory(id=wd_id,
                              branch=branch,
                              path=wd_path(workdirs_root, wd_id),
                              )
        new_rosterf.writelines(other_lines)
        new_rosterf.write(wd.roster_line(pid=current_pid))
    return wd


def release_workdir(repo, wd):
    with locked_roster(repo) as (rosterf, new_rosterf):
        for parsed, line in roster_iter(rosterf):
            if parsed[0] != wd.id:
                new_rosterf.write(line)
            new_rosterf.write(wd.roster_line(pid=None))


def workdirs_gc(workdirs_root, repo, max_age_seconds, now=None):
    """Purge working directories that have not been used for long.

    At least one working directory for the GitLab default branch is
    always kept.
    If later on we start seeding working directories from other working
    directories, even if branches differ (it could indeed be faster on
    average), then we might want to always keep at least one, just preferably
    for the default branch if possible.

    In case a removal fails, the corresponding roster line is kept for
    consistency, and so that subsequent allocation does not end in error
    (assuming the disk is working again anyway).

    :param max_age: time, in seconds since last time the working directory
       was used.
    :param now: current time in seconds since Unix epoch (should be used in
       tests only)
    """
    if now is None:
        now = time.time()

    # using gitlab_revision_changeset spares us the back-and-forth between
    # GitLab and Mercurial branches, with its special cases (topic…)
    head = gitlab_revision_changeset(repo, b'HEAD')
    default_branch = None if head is None else head.branch()
    default_branch_kept = False
    to_remove = {}
    to_keep = []
    with locked_roster(repo) as (rosterf, new_rosterf):
        for (wd_id, pid, timestamp, branch), line in roster_iter(rosterf):
            if pid is None and now - timestamp > max_age_seconds:
                to_remove.setdefault(branch, []).append((wd_id, line))
            else:
                to_keep.append(line)
                if branch == default_branch:
                    default_branch_kept = True

        if not default_branch_kept:
            default_branch_to_rm = to_remove.get(default_branch)
            if default_branch_to_rm:
                to_keep.append(default_branch_to_rm.pop()[1])

        for _, to_rm in to_remove.items():
            for wd_id, line in to_rm:
                path = wd_path(workdirs_root, wd_id)
                try:
                    shutil.rmtree(path)
                except Exception:
                    logger.exception("Failed to remove working directory '%s' "
                                     "for repo at %r", path, repo.root)
                    to_keep.append(line)

        new_rosterf.writelines(to_keep)
