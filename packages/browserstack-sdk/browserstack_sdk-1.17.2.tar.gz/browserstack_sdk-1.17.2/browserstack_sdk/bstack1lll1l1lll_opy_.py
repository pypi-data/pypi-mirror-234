# coding: UTF-8
import sys
bstack1lllll1l_opy_ = sys.version_info [0] == 2
bstack11llll_opy_ = 2048
bstack11111ll_opy_ = 7
def bstack1lllll_opy_ (bstack1l1lll1_opy_):
    global bstack1l1l11_opy_
    bstack1lll1ll_opy_ = ord (bstack1l1lll1_opy_ [-1])
    bstack11lll_opy_ = bstack1l1lll1_opy_ [:-1]
    bstack1lll11_opy_ = bstack1lll1ll_opy_ % len (bstack11lll_opy_)
    bstack11111l1_opy_ = bstack11lll_opy_ [:bstack1lll11_opy_] + bstack11lll_opy_ [bstack1lll11_opy_:]
    if bstack1lllll1l_opy_:
        bstack1ll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11llll_opy_ - (bstack1111ll_opy_ + bstack1lll1ll_opy_) % bstack11111ll_opy_) for bstack1111ll_opy_, char in enumerate (bstack11111l1_opy_)])
    else:
        bstack1ll1l1_opy_ = str () .join ([chr (ord (char) - bstack11llll_opy_ - (bstack1111ll_opy_ + bstack1lll1ll_opy_) % bstack11111ll_opy_) for bstack1111ll_opy_, char in enumerate (bstack11111l1_opy_)])
    return eval (bstack1ll1l1_opy_)
import threading
class bstack111l1ll1_opy_(threading.Thread):
    def run(self):
        self.exc = None
        try:
            self.ret = self._target(*self._args, **self._kwargs)
        except Exception as e:
            self.exc = e
    def join(self, timeout=None):
        super(bstack111l1ll1_opy_, self).join(timeout)
        if self.exc:
            raise self.exc
        return self.ret