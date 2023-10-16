# Copyright 2020-2023 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later

import grpc
import pytest
import re

from hgitaly.stub.repository_pb2 import (
    ApplyGitattributesRequest,
)
from hgitaly.stub.ref_pb2 import FindTagError
from hgitaly.stub.errors_pb2 import ReferenceNotFoundError
from hgitaly.stub.repository_pb2_grpc import RepositoryServiceStub

from ..errors import (
    structured_abort
)
from ..testing.context import FakeServicerContext

StatusCode = grpc.StatusCode


def test_not_implemented(grpc_channel):
    repo_stub = RepositoryServiceStub(grpc_channel)

    with pytest.raises(grpc.RpcError) as exc_info:
        repo_stub.ApplyGitattributes(ApplyGitattributesRequest())
    exc = exc_info.value

    assert exc.code() == grpc.StatusCode.UNIMPLEMENTED
    assert re.search('https://.*/-/issues/1234567', exc.details()) is not None


class FakeContext(FakeServicerContext):

    _trailing_metadata = _code = _details = None

    def set_trailing_metadata(self, metadata):
        self._trailing_metadata = metadata

    def trailing_metadata(self):
        return self._trailing_metadata

    def code(self):
        return self._code

    def details(self):
        return self._details

    def abort(self, code, details):
        self._code = code
        self._details = details
        raise RuntimeError('abort-from-tests')


def test_structured_abort():
    context = FakeContext()

    # example as close as real life as it gets: found with Gitaly Comparison
    # tests in a call for a non-existing tag.
    with pytest.raises(RuntimeError):
        structured_abort(
            context, StatusCode.NOT_FOUND, "tag does not exist",
            FindTagError(
                tag_not_found=ReferenceNotFoundError(
                    reference_name=b"refs/tags/nosuchtag")
            ))
    assert context.code() == StatusCode.NOT_FOUND
    assert context.details() == "tag does not exist"
    trailing = context.trailing_metadata()
    assert len(trailing) == 1
    assert trailing[0] == ('grpc-status-details-bin',
                           b"\x08\x05\x12\x12tag does not exist\x1aB\n'"
                           b"type.googleapis.com/gitaly.FindTagError\x12\x17\n"
                           b"\x15\n\x13refs/tags/nosuchtag")
