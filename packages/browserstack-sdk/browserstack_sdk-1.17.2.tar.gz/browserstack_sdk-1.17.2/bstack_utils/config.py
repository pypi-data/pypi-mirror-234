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
conf = {
    bstack1lllll_opy_ (u"ࠫࡦࡶࡰࡠࡣࡸࡸࡴࡳࡡࡵࡧࠪ೐"): False,
    bstack1lllll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭೑"): True,
}
class Config(object):
    instance = None
    def __init__(self):
        self._1ll11l11l1_opy_ = conf
    @classmethod
    def get_instance(cls):
        if cls.instance:
            return cls.instance
        return Config()
    def get_property(self, property_name):
        return self._1ll11l11l1_opy_.get(property_name, None)
    def bstack1lllll1l1_opy_(self, property_name, bstack1ll11l11ll_opy_):
        self._1ll11l11l1_opy_[property_name] = bstack1ll11l11ll_opy_