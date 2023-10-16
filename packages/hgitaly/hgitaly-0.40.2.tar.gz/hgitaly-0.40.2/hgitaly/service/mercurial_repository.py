# coding: utf-8
# Copyright 2021 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
import logging
import os

from grpc import StatusCode

from mercurial import (
    exchange,
    pycompat,
)

from ..branch import iter_gitlab_branches_matching
from ..peer import (
    FileURLOutsidePath,
    InvalidURLScheme,
    PeerInitException,
    URLParseError,
    hg_remote_peer,
)
from ..repository import (
    config_inherits,
    heptapod_config,
    heptapod_local_config,
    set_config_inheritance,
    set_managed_config,
)
from ..errors import (
    not_implemented,
)
from ..stub.mercurial_repository_pb2 import (
    ConfigItemType,
    GetConfigItemRequest,
    GetConfigItemResponse,
    GetManagedConfigRequest,
    GetManagedConfigResponse,
    PushRequest,
    PushResponse,
    SetManagedConfigRequest,
    SetManagedConfigResponse,
)
from ..stub.mercurial_repository_pb2_grpc import (
    MercurialRepositoryServiceServicer,
)
from ..servicer import HGitalyServicer

logger = logging.getLogger(__name__)


class MercurialRepositoryServicer(MercurialRepositoryServiceServicer,
                                  HGitalyServicer):
    """MercurialRepositoryService implementation.

    The ordering of methods in this source file is the same as in the proto
    file.
    """
    def GetConfigItem(self,
                      request: GetConfigItemRequest,
                      context) -> GetConfigItemResponse:
        repo = self.load_repo(request.repository, context)
        section = pycompat.sysbytes(request.section)
        name = pycompat.sysbytes(request.name)

        if request.as_type == ConfigItemType.BOOL:
            # TODO error treatment if value is not boolean
            return GetConfigItemResponse(
                as_bool=repo.ui.configbool(section, name))

        not_implemented(context, issue=60)  # pragma no cover

    def GetManagedConfig(self,
                         request: GetManagedConfigRequest,
                         context) -> GetManagedConfigResponse:
        repo = self.load_repo(request.repository, context)
        if request.local:
            heptapod_section = heptapod_local_config(repo)
        else:
            heptapod_section = heptapod_config(repo)
        return GetManagedConfigResponse(inherit=config_inherits(repo),
                                        heptapod=heptapod_section)

    def SetManagedConfig(self,
                         request: SetManagedConfigRequest,
                         context) -> SetManagedConfigResponse:
        repo = self.load_repo(request.repository, context)
        set_managed_config(repo,
                           heptapod=request.heptapod,
                           remove_items=request.remove_items,
                           by_line=request.by_line)
        if request.HasField('inherit'):
            if not request.inherit:
                hgrc_dir = None  # remove
            else:
                project_path = request.repository.gl_project_path
                group_path = project_path.rsplit('/', 1)[0]
                hgrc_dir = os.path.relpath(
                    group_path,
                    request.repository.relative_path + '/.hg'
                )
            set_config_inheritance(repo, hgrc_dir, request.by_line)

        return SetManagedConfigResponse()

    def Push(self, request: PushRequest, context) -> PushResponse:
        repo = self.load_repo(request.repository, context)
        repo.ui.setconfig(b'hooks', b'pretxnclose.heptapod_sync', b'')
        repo.ui.setconfig(b'experimental', b'auto-publish', b'abort')

        remote_url = request.remote_peer.url

        # storage name has already been validated by the repository resolution
        storage_path = os.fsdecode(
            self.storages.get(request.repository.storage_name))

        try:
            with hg_remote_peer(repo, request.remote_peer,
                                storage_path=storage_path) as remote_peer:
                include_drafts = request.include_drafts
                only_revs = None
                only_branches_matching = request.only_gitlab_branches_matching
                if only_branches_matching:
                    only_heads = [
                        ctx.hex()
                        for _name, ctx in iter_gitlab_branches_matching(
                            repo, only_branches_matching)
                    ]
                    if include_drafts:
                        only_revs = repo.revs('%ls', only_heads)
                    else:
                        # Note that this is public ancestors of the given
                        # heads,  not the same as ancestors of public heads.
                        # This form is preferred because it doesn't block the
                        # push of the protected branch if its head happens
                        # to be a draft.
                        only_revs = repo.revs('public() and ::(%ls)',
                                              only_heads)
                elif not include_drafts:
                    only_revs = repo.revs('public()')

                if only_revs is not None and not only_revs:
                    return PushResponse(new_changesets=False)

                push_kwargs = dict(newbranch=True)
                if only_revs is not None:
                    push_kwargs['revs'] = [repo[rev].node()
                                           for rev in only_revs]

                try:
                    pushop = exchange.push(repo=repo, remote=remote_peer,
                                           **push_kwargs)
                except Exception as exc:
                    context.abort(StatusCode.INTERNAL,
                                  "Error pushing to %r: %s" % (remote_url,
                                                               exc))

                new_changesets = (pushop.cgresult != 0
                                  and pushop.cgresult is not None)
                return PushResponse(new_changesets=new_changesets)
        except URLParseError as exc:
            context.abort(StatusCode.INVALID_ARGUMENT,
                          "Invalid URL %r for push: %s " % exc.args)
        except InvalidURLScheme as exc:
            context.abort(StatusCode.INVALID_ARGUMENT,
                          "Invalid scheme %r for push URL %r. "
                          "Please use one of %r" % (exc.args[0],
                                                    remote_url, exc.args[1]))
        except FileURLOutsidePath as exc:
            context.abort(StatusCode.INVALID_ARGUMENT,
                          "file URL %r not under storage %r "
                          "root directory" % exc.args)
        except PeerInitException as exc:
            context.abort(StatusCode.INVALID_ARGUMENT,
                          "URL %r could not be used as "
                          "a peer for push: %s" % (remote_url, exc))
        except Exception as exc:
            code = context.code()
            if code is not None and code != StatusCode.OK:
                # already treated: context.abort() raises Exception() (sic)
                raise

            context.abort(StatusCode.INTERNAL,
                          "Unexpected error, not in the actual "
                          "push to %r: %s" % (remote_url, exc))
