# Copyright 2020-2023 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
from grpc import StatusCode
from google.protobuf.any_pb2 import Any
from google.rpc.status_pb2 import Status
import logging

logger = logging.getLogger(__name__)

HGITALY_ISSUES_URL = "https://foss.heptapod.net/heptapod/hgitaly/-/issues"


class ServiceError(RuntimeError):
    """An exception class to complement setting of context.

    In cases where a more precise exception than the bare `Exception()` raised
    by `ServicerContext.abort()` is useful.

    Caller is expected to set code and optionally details.
    """


def not_implemented(context, issue: int):
    """Raise with NOT_IMPLEMENTED status code and link to issue.
    """
    msg = "Not implemented. Tracking issue: %s/%d" % (HGITALY_ISSUES_URL,
                                                      issue)
    logger.error(msg)
    context.abort(StatusCode.UNIMPLEMENTED, msg)


def structured_abort(context, code, msg, structured_error):
    """Abort method with Gitaly's structured error.
    """
    metadata = context.trailing_metadata()
    # ensure mutability (as a list since that is how we'll do it)
    metadata = [] if metadata is None else list(metadata)

    as_grpc_any = Any()
    as_grpc_any.Pack(structured_error)
    status = Status(code=code.value[0], message=msg, details=[as_grpc_any])
    metadata.append(('grpc-status-details-bin', status.SerializeToString()))
    context.set_trailing_metadata(metadata)
    context.abort(code, msg)
