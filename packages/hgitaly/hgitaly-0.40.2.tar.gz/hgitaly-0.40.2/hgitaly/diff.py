# Copyright 2022 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
"""Utilities for comparison of content between changesets."""
from mercurial import (
    copies,
    diffutil,
    match as matchmod,
    patch as patchmod,
)

from .file_context import git_perms
from .git import (
    OBJECT_MODE_DOES_NOT_EXIST,
)

from .stub.diff_pb2 import (
    ChangedPaths,
    DiffStats,
)

Status_Type_Map = dict(
    added=ChangedPaths.Status.ADDED,
    modified=ChangedPaths.Status.MODIFIED,
    removed=ChangedPaths.Status.DELETED,
    # Note: Mercurial includes TYPE_CHANGE
    # (symlink, regular file, submodule...etc) in MODIFIED status
)
"""Mapping status object attributes to ChangedPaths enum."""

COPIED = ChangedPaths.Status.COPIED


def changed_paths(repo, from_ctx, to_ctx, base_path):
    if base_path is None:
        matcher = None
        path_trim_at = 0
    else:
        # scmutil's match is more geared towards the CLI
        # `hg log` etc and its include patterns would
        # force us to convert everything to absolute paths
        # since $CWD is not the repo root.
        # It is much simpler to use the lower-level match module.
        matcher = matchmod.match(
            root=repo.root,
            # cwd is required, yet should not be relevant
            # in this case.
            cwd=repo.root,
            patterns=[b'path:' + base_path])
        path_trim_at = len(base_path) + 1

    copied = list(copy_changed_paths(
        from_ctx,
        to_ctx,
        copies.pathcopies(from_ctx, to_ctx, match=matcher),
        trim_at=path_trim_at))
    copied_paths = set(cp.path for cp in copied)

    status = from_ctx.status(to_ctx, match=matcher)
    for path in status_changed_paths(from_ctx, to_ctx, status,
                                     trim_at=path_trim_at):
        if path.path not in copied_paths:
            yield path

    yield from iter(copied)


def status_changed_paths(from_ctx, to_ctx, status, trim_at=0):
    """Return ChangedPaths from Mercurial status object"""
    for stype in ['added', 'modified', 'removed']:
        for path in status.__getattribute__(stype):
            if stype == 'added':
                old_mode = OBJECT_MODE_DOES_NOT_EXIST
            else:
                old_mode = git_perms(from_ctx.filectx(path))

            if stype == 'removed':
                new_mode = OBJECT_MODE_DOES_NOT_EXIST
            else:
                new_mode = git_perms(to_ctx.filectx(path))

            yield ChangedPaths(
                path=path[trim_at:],
                old_mode=old_mode,
                new_mode=new_mode,
                status=Status_Type_Map[stype]
            )


def copy_changed_paths(from_ctx, to_ctx, path_copies, trim_at=0):
    """Return ChangedPaths for the given paths, relative to base_path.

    Given that Gitaly currently (gitaly@c54d613d0) does not pass
    `--find-copies-harder` to `git diff-tree`, we cannot be sure of
    what is expected. That being said, `git diff-tree` gives the permission
    at source path as `old_mode`, so we're doing the same.
    """
    for target, source in path_copies.items():
        yield ChangedPaths(path=target[trim_at:],
                           status=COPIED,
                           old_mode=git_perms(to_ctx.filectx(source)),
                           new_mode=git_perms(to_ctx.filectx(target)),
                           )


def chunk_old_new_file_path(header):
    """Return a tuple of (old, new) file path for a diff chunk header
    """
    fname = header.filename()
    from_path, to_path = fname, fname
    if len(header.files()) > 1:
        # file is renamed
        from_path, to_path = header.files()
    return from_path, to_path


def chunk_additions_deletions(header):
    """Return the pair (addition, deletions) for a diff chunk header."""
    adds, dels = 0, 0
    for hunk in header.hunks:
        add_count, del_count = hunk.countchanges(hunk.hunk)
        adds += add_count
        dels += del_count
    return adds, dels


def chunk_stats(chunks):
    """Yield the DiffStats messages from the given diff chunks"""
    for header in patchmod.parsepatch(chunks):
        old_path, path = chunk_old_new_file_path(header)
        if old_path == path:
            old_path = b''
        adds, dels = chunk_additions_deletions(header)
        yield DiffStats(
            path=path,
            old_path=old_path,
            additions=adds,
            deletions=dels,
        )


def diff_opts(repo, git=True):
    opts = {b'git': git}
    return diffutil.difffeatureopts(repo.ui, opts=opts, git=git)
