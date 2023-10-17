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
import json
import os
from bstack_utils.helper import bstack1ll111111l_opy_, bstack111lll11l_opy_, bstack1llll1lll1_opy_, \
    bstack1ll11111ll_opy_
def bstack1ll111ll_opy_(bstack1l1l11l1l1_opy_):
    for driver in bstack1l1l11l1l1_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1l11l11l1_opy_(type, name, status, reason, bstack1111l11ll_opy_, bstack11l1111l1_opy_):
    bstack1l1l1l11_opy_ = {
        bstack1lllll_opy_ (u"ࠫࡦࡩࡴࡪࡱࡱࠫ၂"): type,
        bstack1lllll_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨ၃"): {}
    }
    if type == bstack1lllll_opy_ (u"࠭ࡡ࡯ࡰࡲࡸࡦࡺࡥࠨ၄"):
        bstack1l1l1l11_opy_[bstack1lllll_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪ၅")][bstack1lllll_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ၆")] = bstack1111l11ll_opy_
        bstack1l1l1l11_opy_[bstack1lllll_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ၇")][bstack1lllll_opy_ (u"ࠪࡨࡦࡺࡡࠨ၈")] = json.dumps(str(bstack11l1111l1_opy_))
    if type == bstack1lllll_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ၉"):
        bstack1l1l1l11_opy_[bstack1lllll_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨ၊")][bstack1lllll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ။")] = name
    if type == bstack1lllll_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠪ၌"):
        bstack1l1l1l11_opy_[bstack1lllll_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫ၍")][bstack1lllll_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ၎")] = status
        if status == bstack1lllll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ၏") and str(reason) != bstack1lllll_opy_ (u"ࠦࠧၐ"):
            bstack1l1l1l11_opy_[bstack1lllll_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨၑ")][bstack1lllll_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭ၒ")] = json.dumps(str(reason))
    bstack1l1l1lll_opy_ = bstack1lllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠬၓ").format(json.dumps(bstack1l1l1l11_opy_))
    return bstack1l1l1lll_opy_
def bstack111l11111_opy_(url, config, logger, bstack11111lll1_opy_=False):
    hostname = bstack111lll11l_opy_(url)
    is_private = bstack1llll1lll1_opy_(hostname)
    try:
        if is_private or bstack11111lll1_opy_:
            file_path = bstack1ll111111l_opy_(bstack1lllll_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨၔ"), bstack1lllll_opy_ (u"ࠩ࠱ࡦࡸࡺࡡࡤ࡭࠰ࡧࡴࡴࡦࡪࡩ࠱࡮ࡸࡵ࡮ࠨၕ"), logger)
            if os.environ.get(bstack1lllll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡐࡒࡘࡤ࡙ࡅࡕࡡࡈࡖࡗࡕࡒࠨၖ")) and eval(
                    os.environ.get(bstack1lllll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡑࡓ࡙ࡥࡓࡆࡖࡢࡉࡗࡘࡏࡓࠩၗ"))):
                return
            if (bstack1lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩၘ") in config and not config[bstack1lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪၙ")]):
                os.environ[bstack1lllll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡔࡏࡕࡡࡖࡉ࡙ࡥࡅࡓࡔࡒࡖࠬၚ")] = str(True)
                bstack1l1l11l11l_opy_ = {bstack1lllll_opy_ (u"ࠨࡪࡲࡷࡹࡴࡡ࡮ࡧࠪၛ"): hostname}
                bstack1ll11111ll_opy_(bstack1lllll_opy_ (u"ࠩ࠱ࡦࡸࡺࡡࡤ࡭࠰ࡧࡴࡴࡦࡪࡩ࠱࡮ࡸࡵ࡮ࠨၜ"), bstack1lllll_opy_ (u"ࠪࡲࡺࡪࡧࡦࡡ࡯ࡳࡨࡧ࡬ࠨၝ"), bstack1l1l11l11l_opy_, logger)
    except Exception as e:
        pass
def bstack11111ll1l_opy_(caps, bstack1l1l11l1ll_opy_):
    if bstack1lllll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬၞ") in caps:
        caps[bstack1lllll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ၟ")][bstack1lllll_opy_ (u"࠭࡬ࡰࡥࡤࡰࠬၠ")] = True
        if bstack1l1l11l1ll_opy_:
            caps[bstack1lllll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨၡ")][bstack1lllll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪၢ")] = bstack1l1l11l1ll_opy_
    else:
        caps[bstack1lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࠧၣ")] = True
        if bstack1l1l11l1ll_opy_:
            caps[bstack1lllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫၤ")] = bstack1l1l11l1ll_opy_