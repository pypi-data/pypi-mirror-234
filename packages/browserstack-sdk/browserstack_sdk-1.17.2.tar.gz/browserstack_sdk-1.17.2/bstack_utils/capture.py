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
import sys
class bstack1ll11l1l11_opy_:
    def __init__(self, handler):
        self._1ll11ll111_opy_ = sys.stdout.write
        self._1ll11l1ll1_opy_ = sys.stderr.write
        self.handler = handler
        self._started = False
    def start(self):
        if self._started:
            return
        self._started = True
        sys.stdout.write = self.bstack1ll11l1l1l_opy_
        sys.stdout.error = self.bstack1ll11l1lll_opy_
    def bstack1ll11l1l1l_opy_(self, _str):
        self._1ll11ll111_opy_(_str)
        if self.handler:
            self.handler({bstack1lllll_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫೊ"): bstack1lllll_opy_ (u"࠭ࡉࡏࡈࡒࠫೋ"), bstack1lllll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨೌ"): _str})
    def bstack1ll11l1lll_opy_(self, _str):
        self._1ll11l1ll1_opy_(_str)
        if self.handler:
            self.handler({bstack1lllll_opy_ (u"ࠨ࡮ࡨࡺࡪࡲ್ࠧ"): bstack1lllll_opy_ (u"ࠩࡈࡖࡗࡕࡒࠨ೎"), bstack1lllll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ೏"): _str})
    def reset(self):
        if not self._started:
            return
        self._started = False
        sys.stdout.write = self._1ll11ll111_opy_
        sys.stderr.write = self._1ll11l1ll1_opy_