# Copyright 2023 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
import attr
import contextlib
from .comparison import BaseRpcHelper


@attr.s
class HGitalyRHGitalyComparison():
    """This fixture is for comparison between HGitaly and RHGitaly.

    Gitaly itself is not involved at all, so this is for HGitaly-specific
    calls, often but not necessarily involving the Mercurial services.
    """
    hgitaly_channel = attr.ib()
    rhgitaly_channel = attr.ib()

    server_repos_root = attr.ib(default=None)  # not used yet

    def rpc_helper(self, **kw):
        return RpcHelper(self, **kw)


class RpcHelper(BaseRpcHelper):
    """Encapsulates a comparison fixture with call and compare helpers.

    This is derived from :class:`hgitaly.comparison.RpcHelper`, but it is
    very much simpler.
    """
    def init_stubs(self):
        comparison, stub_cls = self.comparison, self.stub_cls
        self.stubs = dict(hgitaly=stub_cls(comparison.hgitaly_channel),
                          rhgitaly=stub_cls(comparison.rhgitaly_channel))

    def assert_compare(self, **kwargs):
        self.apply_request_defaults(kwargs)
        assert self.rpc('hgitaly', **kwargs) == self.rpc('rhgitaly', **kwargs)


@contextlib.contextmanager
def hgitaly_rhgitaly_comparison_fixture(server_repos_root,
                                        hgitaly_channel,
                                        rhgitaly_channel,
                                        ):
    yield HGitalyRHGitalyComparison(hgitaly_channel=hgitaly_channel,
                                    rhgitaly_channel=rhgitaly_channel)
