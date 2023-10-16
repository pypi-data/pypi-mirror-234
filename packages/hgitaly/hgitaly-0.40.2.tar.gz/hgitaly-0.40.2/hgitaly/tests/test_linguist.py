# Copyright 2023 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
import pytest
from grpc import StatusCode

from ..linguist import (
    language_stats,
)
from ..testing.context import FakeServicerContext


class FakeContextAbort(RuntimeError):
    pass


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
        raise FakeContextAbort()


def test_tokei_subprocesss_errors(tmpdir):
    bin_path = tmpdir / 'tokei'
    context = FakeContext()
    with pytest.raises(FakeContextAbort):
        language_stats(bin_path, tmpdir / 'tree', context)
    assert context.code() == StatusCode.INTERNAL
    assert "not found" in context.details()

    bin_path.write_binary(b'#!/bin/sh\n\n echo "oops" >&2; exit 3\n')
    with pytest.raises(FakeContextAbort):
        language_stats(bin_path, tmpdir / 'tree', context)
    assert "permission denied" in context.details()

    bin_path.chmod(0o755)

    with pytest.raises(FakeContextAbort):
        language_stats(bin_path, tmpdir / 'tree', context)
    assert context.code() == StatusCode.INTERNAL
    assert "status code=3" in context.details()
    assert "oops" in context.details()

    bin_path.write_binary(b'#!/bin/sh\n\n echo "tokei not-a-version"\n')
    with pytest.raises(FakeContextAbort):
        language_stats(bin_path, tmpdir / 'tree', context)
    assert context.code() == StatusCode.INTERNAL
    assert "Tokei version" in context.details()
    assert "'tokei not-a-version'" in context.details()
