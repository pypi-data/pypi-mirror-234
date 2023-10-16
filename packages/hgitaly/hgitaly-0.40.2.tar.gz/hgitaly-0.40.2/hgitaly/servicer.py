# Copyright 2020 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
from contextlib import contextmanager
import gc
import logging
import os
from pathlib import Path
import time
import weakref

from grpc import StatusCode
from mercurial import (
    error,
    hg,
    ui as uimod,
)
from mercurial.repoview import _filteredrepotypes

from .workdir import working_directory
from .stub.shared_pb2 import (
    Repository,
)

GARBAGE_COLLECTING_RATE_GEN2 = 250
GARBAGE_COLLECTING_RATE_GEN1 = 20

logger = logging.getLogger(__name__)


def clear_repo_class(repo_class):
    _filteredrepotypes.pop(repo_class, None)


repos_counter = 0


def gc_collect(generation):
    logger.info("A total of %d repository objects have been "
                "instantiated in this thread since startup. "
                "Garbage collecting (generation %d)",
                repos_counter, generation)
    start = time.time()
    gc_result = gc.collect(generation=generation)
    logger.info("Garbage collection (generation %d) "
                "done in %f seconds "
                "(%d unreachable objects). Current GC stats: %r",
                generation, time.time() - start, gc_result, gc.get_stats())


def normalize_rpath(gl_repo: Repository):
    rpath = gl_repo.relative_path
    if rpath.endswith('.git'):
        rpath = rpath[:-4] + '.hg'
    return rpath


class HGitalyServicer:
    """Common features of all HGitaly services.

    Attributes:

    - :attr:`storages`: a :class:`dict` mapping storage names to corresponding
      root directory absolute paths, which are given as bytes since we'll have
      to convert paths to bytes anyway, which is the only promise a filesystem
      can make, and what Mercurial expects.
    - :attr:`ui`: base :class:`mercurial.ui.ui` instance from which repository
      uis are derived. In particular, it bears the common configuration.
    """

    STATUS_CODE_STORAGE_NOT_FOUND = StatusCode.NOT_FOUND
    STATUS_CODE_REPO_NOT_FOUND = StatusCode.NOT_FOUND
    STATUS_CODE_MISSING_REPO_ARG = StatusCode.INVALID_ARGUMENT

    def __init__(self, storages):
        self.storages = storages
        self.init_ui()

    def init_ui(self):
        """Prepare the base ``ui`` instance from which all will derive.

        See also :meth:`hgweb.__init__`
        """

        ui = self.ui = uimod.ui.load()
        # prevents `ui.interactive()` to crash (see heptapod#717)
        ui.setconfig(b'ui', b'nontty', b'true', b'hgitaly')

        # progress bars in stdout (log file at best) would be rather useless
        ui.setconfig(b'progress', b'disable', b'true', b'hgitaly')

        # other settings done in hgweb.__init__():
        #
        # - forcing file pattern resolution to be relative to root would be
        #   nice, but perhaps need more adaptation, and would have to be
        #   done in load_repo()
        # - `signal-safe-locks=no` worth being considered, but this not being
        #   WSGI, we control the server and its signal handling (see hgweb's
        #   comment)
        # - `report_unstrusted=off`: if some perms are unaligned, reporting
        #   the untrust could be the only lead for an obscure behaviour
        #   (typically ignoring some settings that can be critical to
        #   operation)

    def load_repo(self, repository: Repository, context):
        """Load the repository from storage name and relative path

        :param repository: Repository Gitaly Message, encoding storage name
            and relative path
        :param context: gRPC context (used in error raising)
        :raises: ``KeyError('storage', storage_name)`` if storage is not found.

        Error treatment: the caller doesn't have to do anything specific,
        the status code and the details are already set in context, and these
        are automatically propagated to the client (see corresponding test
        in `test_servicer.py`). For specific error treatment, use
        :meth:`load_repo_inner` and catch the exceptions it raises.
        """
        try:
            return self.load_repo_inner(repository, context)
        except KeyError as exc:
            self.handle_key_error(context, exc.args)
        except ValueError as exc:
            self.handle_value_error(context, exc.args)

    def handle_value_error(self, context, exc_args):
        context.abort(self.STATUS_CODE_MISSING_REPO_ARG, exc_args[0])

    def handle_key_error(self, context, exc_args):
        ktype = exc_args[0]
        if ktype == 'storage':
            context.abort(self.STATUS_CODE_STORAGE_NOT_FOUND,
                          "No storage named %r" % exc_args[1])
        elif ktype == 'repo':
            context.abort(self.STATUS_CODE_REPO_NOT_FOUND,
                          exc_args[1])

    def load_repo_inner(self, repository: Repository, context):
        """Load the repository from storage name and relative path

        :param repository: Repository Gitaly Message, encoding storage name
            and relative path
        :param context: gRPC context (used in error raising)
        :raises:
          - ``KeyError('storage', storage_name)`` if storage is not found
          - ``KeyError('repo', path, details)`` if repo not found or
            cannot be loaded.
        """
        global repos_counter
        if repos_counter % GARBAGE_COLLECTING_RATE_GEN2 == 0:
            gc_collect(2)
        elif repos_counter % GARBAGE_COLLECTING_RATE_GEN1 == 0:
            gc_collect(1)

        repos_counter += 1

        # shamelessly taken from heptapod.wsgi for the Hgitaly bootstrap
        # note that Gitaly Repository has more than just a relative path,
        # we'll have to decide what we make of the extra information
        repo_path = self.repo_disk_path(repository, context)
        logger.debug("loading repo at %r", repo_path)

        try:
            repo = hg.repository(self.ui, repo_path)
        except error.RepoError as exc:
            raise KeyError('repo', repo_path, repr(exc.args))

        weakref.finalize(repo, clear_repo_class, repo.unfiltered().__class__)
        srcrepo = hg.sharedreposource(repo)
        if srcrepo is not None:
            weakref.finalize(srcrepo, clear_repo_class,
                             srcrepo.unfiltered().__class__)

        return repo

    def storage_root_dir(self, storage_name, context):
        """Return the storage directory.

        If the storage is unknown, this raises
        ``KeyError('storage', storage_name)``
        """
        if not storage_name:
            # this is the best detection of a missing `repository` field
            # in request, without having the request object itself
            raise ValueError('empty repository')

        root_dir = self.storages.get(storage_name)
        if root_dir is None:
            raise KeyError('storage', storage_name)
        return root_dir

    def repo_disk_path(self, repository: Repository, context):
        rpath = normalize_rpath(repository)
        root_dir = self.storage_root_dir(repository.storage_name, context)

        # GitLab filesystem paths are always ASCII
        repo_path = os.path.join(root_dir, rpath.encode('ascii'))
        return repo_path

    def temp_dir(self, storage_name, context, ensure=True):
        """Return the path to temporary directory for the given storage

        Similar to what Gitaly uses, with a dedicated path in order
        to be really sure not to overwrite anything. The important feature
        is that the temporary directory is under the root directory of
        the storage, hence on the same file system (atomic renames of
        other files from the storage, etc.)

        :param bool ensure: if ``True``, the temporary directory is created
           if it does not exist yet.
        """
        try:
            return self.temp_dir_inner(storage_name, context, ensure=ensure)
        except KeyError as exc:
            self.handle_key_error(context, exc.args)
        except ValueError as exc:
            self.handle_value_error(context, exc.args)
        except OSError as exc:
            context.abort(StatusCode.INTERNAL,
                          "Error ensuring temporary dir: %s" % exc)

    def temp_dir_inner(self, storage_name, context, ensure=True):
        """Return the path to temporary directory for the given storage

        Similar to what Gitaly uses, with a dedicated path in order
        to be really sure not to overwrite anything. The important feature
        is that the temporary directory is under the root directory of
        the storage, hence on the same file system (atomic renames of
        other files from the storage, etc.)

        :param bool ensure: if ``True``, the temporary directory is created
           if it does not exist yet.
        :raises KeyError: if the storage is unknown
        :raises OSError: if creation fails.
        """
        temp_dir = os.path.join(self.storage_root_dir(storage_name, context),
                                b'+hgitaly', b'tmp')
        if not ensure:
            return temp_dir

        # not the proper time to switch everything to pathlib (operates on
        # str paths, but surrogates returned by os.fsdecode() seem to really
        # work well)
        to_create = []
        current = temp_dir

        while not os.path.exists(current):
            to_create.append(current)
            current = os.path.dirname(current)

        while to_create:
            # same mode as in Gitaly, hence we don't care about groups
            # although this does propagate the setgid bit
            os.mkdir(to_create.pop(), mode=0o755)

        return temp_dir

    @contextmanager
    def working_dir(self, gl_repo: Repository, repo, context, changeset=None):
        """Provide a working directory updated to the given changeset.

        The working directory is part from the pool of reusable working
        directories and created if needed.
        """
        tmp = Path(os.fsdecode(
            self.temp_dir(gl_repo.storage_name, context, ensure=True)
        ))
        rpath = normalize_rpath(gl_repo)

        with working_directory(tmp / 'workdirs' / rpath, repo,
                               changeset=changeset) as wd:
            yield wd
