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
import datetime
import json
import logging
import os
import threading
from bstack_utils.helper import bstack1l1lll1l11_opy_, bstack1l1lll1111_opy_, get_host_info, bstack1ll11111l1_opy_, bstack1l1ll1ll1l_opy_, bstack1l1lllll11_opy_, \
    bstack1l1llll111_opy_, bstack1l1lllllll_opy_, bstack1l11ll1ll_opy_, bstack1l1ll1lll1_opy_, bstack1ll111ll11_opy_, bstack1l1llllll1_opy_
from bstack_utils.bstack1l1l1l11ll_opy_ import bstack1l1l1l11l1_opy_
bstack1l11lll11l_opy_ = [
    bstack1lllll_opy_ (u"ࠫࡑࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࠨၥ"), bstack1lllll_opy_ (u"ࠬࡉࡂࡕࡕࡨࡷࡸ࡯࡯࡯ࡅࡵࡩࡦࡺࡥࡥࠩၦ"), bstack1lllll_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨၧ"), bstack1lllll_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔ࡭࡬ࡴࡵ࡫ࡤࠨၨ"),
    bstack1lllll_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪၩ"), bstack1lllll_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪၪ"), bstack1lllll_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫၫ")
]
bstack1l11l1l11l_opy_ = bstack1lllll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡩ࡯࡭࡮ࡨࡧࡹࡵࡲ࠮ࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫၬ")
logger = logging.getLogger(__name__)
class bstack1lllll111_opy_:
    bstack1l1l1l11ll_opy_ = None
    bs_config = None
    @classmethod
    @bstack1l1llllll1_opy_(class_method=True)
    def launch(cls, bs_config, bstack1l11ll1ll1_opy_):
        cls.bs_config = bs_config
        if not cls.bstack1l11ll11l1_opy_():
            return
        cls.bstack1l1l1l11ll_opy_ = bstack1l1l1l11l1_opy_(cls.bstack1l1l111111_opy_)
        cls.bstack1l1l1l11ll_opy_.start()
        bstack1l11ll1111_opy_ = bstack1ll11111l1_opy_(bs_config)
        bstack1l11lllll1_opy_ = bstack1l1ll1ll1l_opy_(bs_config)
        data = {
            bstack1lllll_opy_ (u"ࠬ࡬࡯ࡳ࡯ࡤࡸࠬၭ"): bstack1lllll_opy_ (u"࠭ࡪࡴࡱࡱࠫၮ"),
            bstack1lllll_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡠࡰࡤࡱࡪ࠭ၯ"): bs_config.get(bstack1lllll_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭ၰ"), bstack1lllll_opy_ (u"ࠩࠪၱ")),
            bstack1lllll_opy_ (u"ࠪࡲࡦࡳࡥࠨၲ"): bs_config.get(bstack1lllll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧၳ"), os.path.basename(os.path.abspath(os.getcwd()))),
            bstack1lllll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨၴ"): bs_config.get(bstack1lllll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨၵ")),
            bstack1lllll_opy_ (u"ࠧࡥࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬၶ"): bs_config.get(bstack1lllll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡄࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫၷ"), bstack1lllll_opy_ (u"ࠩࠪၸ")),
            bstack1lllll_opy_ (u"ࠪࡷࡹࡧࡲࡵࡡࡷ࡭ࡲ࡫ࠧၹ"): datetime.datetime.now().isoformat(),
            bstack1lllll_opy_ (u"ࠫࡹࡧࡧࡴࠩၺ"): bstack1l1lllll11_opy_(bs_config),
            bstack1lllll_opy_ (u"ࠬ࡮࡯ࡴࡶࡢ࡭ࡳ࡬࡯ࠨၻ"): get_host_info(),
            bstack1lllll_opy_ (u"࠭ࡣࡪࡡ࡬ࡲ࡫ࡵࠧၼ"): bstack1l1lll1111_opy_(),
            bstack1lllll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡲࡶࡰࡢ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧၽ"): os.environ.get(bstack1lllll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡗࡌࡐࡉࡥࡒࡖࡐࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧၾ")),
            bstack1lllll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࡡࡷࡩࡸࡺࡳࡠࡴࡨࡶࡺࡴࠧၿ"): os.environ.get(bstack1lllll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࠨႀ"), False),
            bstack1lllll_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࡤࡩ࡯࡯ࡶࡵࡳࡱ࠭ႁ"): bstack1l1lll1l11_opy_(),
            bstack1lllll_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ႂ"): {
                bstack1lllll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡐࡤࡱࡪ࠭ႃ"): bstack1l11ll1ll1_opy_.get(bstack1lllll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥࠨႄ"), bstack1lllll_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴࠨႅ")),
                bstack1lllll_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬႆ"): bstack1l11ll1ll1_opy_.get(bstack1lllll_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧႇ")),
                bstack1lllll_opy_ (u"ࠫࡸࡪ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨႈ"): bstack1l11ll1ll1_opy_.get(bstack1lllll_opy_ (u"ࠬࡹࡤ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪႉ"))
            }
        }
        config = {
            bstack1lllll_opy_ (u"࠭ࡡࡶࡶ࡫ࠫႊ"): (bstack1l11ll1111_opy_, bstack1l11lllll1_opy_),
            bstack1lllll_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨႋ"): cls.default_headers()
        }
        response = bstack1l11ll1ll_opy_(bstack1lllll_opy_ (u"ࠨࡒࡒࡗ࡙࠭ႌ"), cls.request_url(bstack1lllll_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡥࡹ࡮ࡲࡤࡴႍࠩ")), data, config)
        if response.status_code != 200:
            os.environ[bstack1lllll_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡃࡐࡏࡓࡐࡊ࡚ࡅࡅࠩႎ")] = bstack1lllll_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪႏ")
            os.environ[bstack1lllll_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡍ࡛࡙࠭႐")] = bstack1lllll_opy_ (u"࠭࡮ࡶ࡮࡯ࠫ႑")
            os.environ[bstack1lllll_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉ࠭႒")] = bstack1lllll_opy_ (u"ࠣࡰࡸࡰࡱࠨ႓")
            os.environ[bstack1lllll_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡁࡍࡎࡒ࡛ࡤ࡙ࡃࡓࡇࡈࡒࡘࡎࡏࡕࡕࠪ႔")] = bstack1lllll_opy_ (u"ࠥࡲࡺࡲ࡬ࠣ႕")
            bstack1l11l1lll1_opy_ = response.json()
            if bstack1l11l1lll1_opy_ and bstack1l11l1lll1_opy_[bstack1lllll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ႖")]:
                error_message = bstack1l11l1lll1_opy_[bstack1lllll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭႗")]
                if bstack1l11l1lll1_opy_[bstack1lllll_opy_ (u"࠭ࡥࡳࡴࡲࡶ࡙ࡿࡰࡦࠩ႘")] == bstack1lllll_opy_ (u"ࠧࡆࡔࡕࡓࡗࡥࡉࡏࡘࡄࡐࡎࡊ࡟ࡄࡔࡈࡈࡊࡔࡔࡊࡃࡏࡗࠬ႙"):
                    logger.error(error_message)
                elif bstack1l11l1lll1_opy_[bstack1lllll_opy_ (u"ࠨࡧࡵࡶࡴࡸࡔࡺࡲࡨࠫႚ")] == bstack1lllll_opy_ (u"ࠩࡈࡖࡗࡕࡒࡠࡃࡆࡇࡊ࡙ࡓࡠࡆࡈࡒࡎࡋࡄࠨႛ"):
                    logger.info(error_message)
                elif bstack1l11l1lll1_opy_[bstack1lllll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࡖࡼࡴࡪ࠭ႜ")] == bstack1lllll_opy_ (u"ࠫࡊࡘࡒࡐࡔࡢࡗࡉࡑ࡟ࡅࡇࡓࡖࡊࡉࡁࡕࡇࡇࠫႝ"):
                    logger.error(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack1l1ll1l1ll_opy_ (u"ࠧࡊࡡࡵࡣࠣࡹࡵࡲ࡯ࡢࡦࠣࡸࡴࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯࡚ࠥࡥࡴࡶࠣࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠣࡪࡦ࡯࡬ࡦࡦࠣࡨࡺ࡫ࠠࡵࡱࠣࡷࡴࡳࡥࠡࡧࡵࡶࡴࡸࠢ႞"))
            return [None, None, None]
        os.environ[bstack1lllll_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡆࡓࡒࡖࡌࡆࡖࡈࡈࠬ႟")] = bstack1lllll_opy_ (u"ࠧࡵࡴࡸࡩࠬႠ")
        bstack1l11l1lll1_opy_ = response.json()
        if bstack1l11l1lll1_opy_.get(bstack1lllll_opy_ (u"ࠨ࡬ࡺࡸࠬႡ")):
            os.environ[bstack1lllll_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡊࡘࡖࠪႢ")] = bstack1l11l1lll1_opy_[bstack1lllll_opy_ (u"ࠪ࡮ࡼࡺࠧႣ")]
            os.environ[bstack1lllll_opy_ (u"ࠫࡈࡘࡅࡅࡇࡑࡘࡎࡇࡌࡔࡡࡉࡓࡗࡥࡃࡓࡃࡖࡌࡤࡘࡅࡑࡑࡕࡘࡎࡔࡇࠨႤ")] = json.dumps({
                bstack1lllll_opy_ (u"ࠬࡻࡳࡦࡴࡱࡥࡲ࡫ࠧႥ"): bstack1l11ll1111_opy_,
                bstack1lllll_opy_ (u"࠭ࡰࡢࡵࡶࡻࡴࡸࡤࠨႦ"): bstack1l11lllll1_opy_
            })
        if bstack1l11l1lll1_opy_.get(bstack1lllll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩႧ")):
            os.environ[bstack1lllll_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡍࡇࡓࡉࡇࡇࡣࡎࡊࠧႨ")] = bstack1l11l1lll1_opy_[bstack1lllll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫႩ")]
        if bstack1l11l1lll1_opy_.get(bstack1lllll_opy_ (u"ࠪࡥࡱࡲ࡯ࡸࡡࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧႪ")):
            os.environ[bstack1lllll_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡃࡏࡐࡔ࡝࡟ࡔࡅࡕࡉࡊࡔࡓࡉࡑࡗࡗࠬႫ")] = str(bstack1l11l1lll1_opy_[bstack1lllll_opy_ (u"ࠬࡧ࡬࡭ࡱࡺࡣࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠩႬ")])
        return [bstack1l11l1lll1_opy_[bstack1lllll_opy_ (u"࠭ࡪࡸࡶࠪႭ")], bstack1l11l1lll1_opy_[bstack1lllll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩႮ")], bstack1l11l1lll1_opy_[bstack1lllll_opy_ (u"ࠨࡣ࡯ࡰࡴࡽ࡟ࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࡷࠬႯ")]]
    @classmethod
    @bstack1l1llllll1_opy_(class_method=True)
    def stop(cls):
        if not cls.on():
            return
        if os.environ[bstack1lllll_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡊࡘࡖࠪႰ")] == bstack1lllll_opy_ (u"ࠥࡲࡺࡲ࡬ࠣႱ") or os.environ[bstack1lllll_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡄࡘࡍࡑࡊ࡟ࡉࡃࡖࡌࡊࡊ࡟ࡊࡆࠪႲ")] == bstack1lllll_opy_ (u"ࠧࡴࡵ࡭࡮ࠥႳ"):
            print(bstack1lllll_opy_ (u"࠭ࡅ࡙ࡅࡈࡔ࡙ࡏࡏࡏࠢࡌࡒࠥࡹࡴࡰࡲࡅࡹ࡮ࡲࡤࡖࡲࡶࡸࡷ࡫ࡡ࡮ࠢࡕࡉࡖ࡛ࡅࡔࡖࠣࡘࡔࠦࡔࡆࡕࡗࠤࡔࡈࡓࡆࡔ࡙ࡅࡇࡏࡌࡊࡖ࡜ࠤ࠿ࠦࡍࡪࡵࡶ࡭ࡳ࡭ࠠࡢࡷࡷ࡬ࡪࡴࡴࡪࡥࡤࡸ࡮ࡵ࡮ࠡࡶࡲ࡯ࡪࡴࠧႴ"))
            return {
                bstack1lllll_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧႵ"): bstack1lllll_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧႶ"),
                bstack1lllll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪႷ"): bstack1lllll_opy_ (u"ࠪࡘࡴࡱࡥ࡯࠱ࡥࡹ࡮ࡲࡤࡊࡆࠣ࡭ࡸࠦࡵ࡯ࡦࡨࡪ࡮ࡴࡥࡥ࠮ࠣࡦࡺ࡯࡬ࡥࠢࡦࡶࡪࡧࡴࡪࡱࡱࠤࡲ࡯ࡧࡩࡶࠣ࡬ࡦࡼࡥࠡࡨࡤ࡭ࡱ࡫ࡤࠨႸ")
            }
        else:
            cls.bstack1l1l1l11ll_opy_.shutdown()
            data = {
                bstack1lllll_opy_ (u"ࠫࡸࡺ࡯ࡱࡡࡷ࡭ࡲ࡫ࠧႹ"): datetime.datetime.now().isoformat()
            }
            config = {
                bstack1lllll_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡸ࠭Ⴚ"): cls.default_headers()
            }
            bstack1l1lll1lll_opy_ = bstack1lllll_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡢࡶ࡫࡯ࡨࡸ࠵ࡻࡾ࠱ࡶࡸࡴࡶࠧႻ").format(os.environ[bstack1lllll_opy_ (u"ࠢࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉࠨႼ")])
            bstack1l11l1ll11_opy_ = cls.request_url(bstack1l1lll1lll_opy_)
            response = bstack1l11ll1ll_opy_(bstack1lllll_opy_ (u"ࠨࡒࡘࡘࠬႽ"), bstack1l11l1ll11_opy_, data, config)
            if not response.ok:
                raise Exception(bstack1lllll_opy_ (u"ࠤࡖࡸࡴࡶࠠࡳࡧࡴࡹࡪࡹࡴࠡࡰࡲࡸࠥࡵ࡫ࠣႾ"))
    @classmethod
    def bstack1l11ll1l1l_opy_(cls):
        if cls.bstack1l1l1l11ll_opy_ is None:
            return
        cls.bstack1l1l1l11ll_opy_.shutdown()
    @classmethod
    def bstack1lll1ll1ll_opy_(cls):
        if cls.on():
            print(
                bstack1lllll_opy_ (u"࡚ࠪ࡮ࡹࡩࡵࠢ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡢࡶ࡫࡯ࡨࡸ࠵ࡻࡾࠢࡷࡳࠥࡼࡩࡦࡹࠣࡦࡺ࡯࡬ࡥࠢࡵࡩࡵࡵࡲࡵ࠮ࠣ࡭ࡳࡹࡩࡨࡪࡷࡷ࠱ࠦࡡ࡯ࡦࠣࡱࡦࡴࡹࠡ࡯ࡲࡶࡪࠦࡤࡦࡤࡸ࡫࡬࡯࡮ࡨࠢ࡬ࡲ࡫ࡵࡲ࡮ࡣࡷ࡭ࡴࡴࠠࡢ࡮࡯ࠤࡦࡺࠠࡰࡰࡨࠤࡵࡲࡡࡤࡧࠤࡠࡳ࠭Ⴟ").format(os.environ[bstack1lllll_opy_ (u"ࠦࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡄࡘࡍࡑࡊ࡟ࡉࡃࡖࡌࡊࡊ࡟ࡊࡆࠥჀ")]))
    @classmethod
    def bstack1l11l1llll_opy_(cls):
        if cls.bstack1l1l1l11ll_opy_ is not None:
            return
        cls.bstack1l1l1l11ll_opy_ = bstack1l1l1l11l1_opy_(cls.bstack1l1l111111_opy_)
        cls.bstack1l1l1l11ll_opy_.start()
    @classmethod
    def bstack1l11ll1l11_opy_(cls, bstack1l1l111l11_opy_, bstack1l11lll1ll_opy_=bstack1lllll_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡨࡡࡵࡥ࡫ࠫჁ")):
        if not cls.on():
            return
        bstack1l11lll11_opy_ = bstack1l1l111l11_opy_[bstack1lllll_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪჂ")]
        bstack1l1l111l1l_opy_ = {
            bstack1lllll_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨჃ"): bstack1lllll_opy_ (u"ࠨࡖࡨࡷࡹࡥࡓࡵࡣࡵࡸࡤ࡛ࡰ࡭ࡱࡤࡨࠬჄ"),
            bstack1lllll_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫჅ"): bstack1lllll_opy_ (u"ࠪࡘࡪࡹࡴࡠࡇࡱࡨࡤ࡛ࡰ࡭ࡱࡤࡨࠬ჆"),
            bstack1lllll_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡱࡩࡱࡲࡨࡨࠬჇ"): bstack1lllll_opy_ (u"࡚ࠬࡥࡴࡶࡢࡗࡰ࡯ࡰࡱࡧࡧࡣ࡚ࡶ࡬ࡰࡣࡧࠫ჈"),
            bstack1lllll_opy_ (u"࠭ࡌࡰࡩࡆࡶࡪࡧࡴࡦࡦࠪ჉"): bstack1lllll_opy_ (u"ࠧࡍࡱࡪࡣ࡚ࡶ࡬ࡰࡣࡧࠫ჊"),
            bstack1lllll_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩ჋"): bstack1lllll_opy_ (u"ࠩࡋࡳࡴࡱ࡟ࡔࡶࡤࡶࡹࡥࡕࡱ࡮ࡲࡥࡩ࠭჌"),
            bstack1lllll_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬჍ"): bstack1lllll_opy_ (u"ࠫࡍࡵ࡯࡬ࡡࡈࡲࡩࡥࡕࡱ࡮ࡲࡥࡩ࠭჎"),
            bstack1lllll_opy_ (u"ࠬࡉࡂࡕࡕࡨࡷࡸ࡯࡯࡯ࡅࡵࡩࡦࡺࡥࡥࠩ჏"): bstack1lllll_opy_ (u"࠭ࡃࡃࡖࡢ࡙ࡵࡲ࡯ࡢࡦࠪა")
        }.get(bstack1l11lll11_opy_)
        if bstack1l11lll1ll_opy_ == bstack1lllll_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡣࡣࡷࡧ࡭࠭ბ"):
            cls.bstack1l11l1llll_opy_()
            cls.bstack1l1l1l11ll_opy_.add(bstack1l1l111l11_opy_)
        elif bstack1l11lll1ll_opy_ == bstack1lllll_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭გ"):
            cls.bstack1l1l111111_opy_([bstack1l1l111l11_opy_], bstack1l11lll1ll_opy_)
    @classmethod
    @bstack1l1llllll1_opy_(class_method=True)
    def bstack1l1l111111_opy_(cls, bstack1l1l111l11_opy_, bstack1l11lll1ll_opy_=bstack1lllll_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡥࡥࡹࡩࡨࠨდ")):
        config = {
            bstack1lllll_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫე"): cls.default_headers()
        }
        response = bstack1l11ll1ll_opy_(bstack1lllll_opy_ (u"ࠫࡕࡕࡓࡕࠩვ"), cls.request_url(bstack1l11lll1ll_opy_), bstack1l1l111l11_opy_, config)
        bstack1l11l1l1ll_opy_ = response.json()
    @classmethod
    @bstack1l1llllll1_opy_(class_method=True)
    def bstack1l11ll11ll_opy_(cls, bstack1l11lll1l1_opy_):
        bstack1l1l111ll1_opy_ = []
        for log in bstack1l11lll1l1_opy_:
            bstack1l1l111ll1_opy_.append({
                bstack1lllll_opy_ (u"ࠬࡱࡩ࡯ࡦࠪზ"): bstack1lllll_opy_ (u"࠭ࡔࡆࡕࡗࡣࡑࡕࡇࠨთ"),
                bstack1lllll_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ი"): log[bstack1lllll_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧკ")],
                bstack1lllll_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬლ"): log[bstack1lllll_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭მ")],
                bstack1lllll_opy_ (u"ࠫ࡭ࡺࡴࡱࡡࡵࡩࡸࡶ࡯࡯ࡵࡨࠫნ"): {},
                bstack1lllll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ო"): log[bstack1lllll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧპ")],
                bstack1lllll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧჟ"): log[bstack1lllll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨრ")]
            })
        cls.bstack1l11ll1l11_opy_({
            bstack1lllll_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭ს"): bstack1lllll_opy_ (u"ࠪࡐࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࠧტ"),
            bstack1lllll_opy_ (u"ࠫࡱࡵࡧࡴࠩუ"): bstack1l1l111ll1_opy_
        })
    @classmethod
    @bstack1l1llllll1_opy_(class_method=True)
    def bstack1l11l1ll1l_opy_(cls, steps):
        bstack1l11l1l1l1_opy_ = []
        for step in steps:
            bstack1l1l1111l1_opy_ = {
                bstack1lllll_opy_ (u"ࠬࡱࡩ࡯ࡦࠪფ"): bstack1lllll_opy_ (u"࠭ࡔࡆࡕࡗࡣࡘ࡚ࡅࡑࠩქ"),
                bstack1lllll_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ღ"): step[bstack1lllll_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧყ")],
                bstack1lllll_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬშ"): step[bstack1lllll_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ჩ")],
                bstack1lllll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬც"): step[bstack1lllll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ძ")],
                bstack1lllll_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠨწ"): step[bstack1lllll_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࠩჭ")]
            }
            if bstack1lllll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨხ") in step:
                bstack1l1l1111l1_opy_[bstack1lllll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩჯ")] = step[bstack1lllll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪჰ")]
            elif bstack1lllll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫჱ") in step:
                bstack1l1l1111l1_opy_[bstack1lllll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬჲ")] = step[bstack1lllll_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ჳ")]
            bstack1l11l1l1l1_opy_.append(bstack1l1l1111l1_opy_)
        cls.bstack1l11ll1l11_opy_({
            bstack1lllll_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫჴ"): bstack1lllll_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬჵ"),
            bstack1lllll_opy_ (u"ࠩ࡯ࡳ࡬ࡹࠧჶ"): bstack1l11l1l1l1_opy_
        })
    @classmethod
    @bstack1l1llllll1_opy_(class_method=True)
    def bstack1l11lll111_opy_(cls, screenshot):
        cls.bstack1l11ll1l11_opy_({
            bstack1lllll_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧჷ"): bstack1lllll_opy_ (u"ࠫࡑࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࠨჸ"),
            bstack1lllll_opy_ (u"ࠬࡲ࡯ࡨࡵࠪჹ"): [{
                bstack1lllll_opy_ (u"࠭࡫ࡪࡰࡧࠫჺ"): bstack1lllll_opy_ (u"ࠧࡕࡇࡖࡘࡤ࡙ࡃࡓࡇࡈࡒࡘࡎࡏࡕࠩ჻"),
                bstack1lllll_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫჼ"): datetime.datetime.utcnow().isoformat() + bstack1lllll_opy_ (u"ࠩ࡝ࠫჽ"),
                bstack1lllll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫჾ"): screenshot[bstack1lllll_opy_ (u"ࠫ࡮ࡳࡡࡨࡧࠪჿ")],
                bstack1lllll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᄀ"): screenshot[bstack1lllll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᄁ")]
            }]
        }, bstack1l11lll1ll_opy_=bstack1lllll_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࡷࠬᄂ"))
    @classmethod
    @bstack1l1llllll1_opy_(class_method=True)
    def bstack1lll1l1111_opy_(cls, driver):
        bstack1l11ll1lll_opy_ = cls.bstack1l11ll1lll_opy_()
        if not bstack1l11ll1lll_opy_:
            return
        cls.bstack1l11ll1l11_opy_({
            bstack1lllll_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬᄃ"): bstack1lllll_opy_ (u"ࠩࡆࡆ࡙࡙ࡥࡴࡵ࡬ࡳࡳࡉࡲࡦࡣࡷࡩࡩ࠭ᄄ"),
            bstack1lllll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬᄅ"): {
                bstack1lllll_opy_ (u"ࠦࡺࡻࡩࡥࠤᄆ"): cls.bstack1l11ll1lll_opy_(),
                bstack1lllll_opy_ (u"ࠧ࡯࡮ࡵࡧࡪࡶࡦࡺࡩࡰࡰࡶࠦᄇ"): cls.bstack1l11llllll_opy_(driver)
            }
        })
    @classmethod
    def on(cls):
        if os.environ.get(bstack1lllll_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡎ࡜࡚ࠧᄈ"), None) is None or os.environ[bstack1lllll_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡏ࡝ࡔࠨᄉ")] == bstack1lllll_opy_ (u"ࠣࡰࡸࡰࡱࠨᄊ"):
            return False
        return True
    @classmethod
    def bstack1l11ll11l1_opy_(cls):
        return bstack1ll111ll11_opy_(cls.bs_config.get(bstack1lllll_opy_ (u"ࠩࡷࡩࡸࡺࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭ᄋ"), False))
    @staticmethod
    def request_url(url):
        return bstack1lllll_opy_ (u"ࠪࡿࢂ࠵ࡻࡾࠩᄌ").format(bstack1l11l1l11l_opy_, url)
    @staticmethod
    def default_headers():
        headers = {
            bstack1lllll_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪᄍ"): bstack1lllll_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨᄎ"),
            bstack1lllll_opy_ (u"࠭ࡘ࠮ࡄࡖࡘࡆࡉࡋ࠮ࡖࡈࡗ࡙ࡕࡐࡔࠩᄏ"): bstack1lllll_opy_ (u"ࠧࡵࡴࡸࡩࠬᄐ")
        }
        if os.environ.get(bstack1lllll_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡐࡗࡕࠩᄑ"), None):
            headers[bstack1lllll_opy_ (u"ࠩࡄࡹࡹ࡮࡯ࡳ࡫ࡽࡥࡹ࡯࡯࡯ࠩᄒ")] = bstack1lllll_opy_ (u"ࠪࡆࡪࡧࡲࡦࡴࠣࡿࢂ࠭ᄓ").format(os.environ[bstack1lllll_opy_ (u"ࠦࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡌ࡚ࡘࠧᄔ")])
        return headers
    @staticmethod
    def bstack1l11ll1lll_opy_():
        return getattr(threading.current_thread(), bstack1lllll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩᄕ"), None)
    @staticmethod
    def bstack1l11llllll_opy_(driver):
        return {
            bstack1l1lllllll_opy_(): bstack1l1llll111_opy_(driver)
        }
    @staticmethod
    def bstack1l11l1l111_opy_(exception_info, report):
        return [{bstack1lllll_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩᄖ"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack1l11llll1l_opy_(typename):
        if bstack1lllll_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࠥᄗ") in typename:
            return bstack1lllll_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࡉࡷࡸ࡯ࡳࠤᄘ")
        return bstack1lllll_opy_ (u"ࠤࡘࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡊࡸࡲࡰࡴࠥᄙ")
    @staticmethod
    def bstack1l11llll11_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1lllll111_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack1l1l11111l_opy_(test):
        bstack1l1l111lll_opy_ = test.parent
        scope = []
        while bstack1l1l111lll_opy_ is not None:
            scope.append(bstack1l1l111lll_opy_.name)
            bstack1l1l111lll_opy_ = bstack1l1l111lll_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1l1l1111ll_opy_(hook_type):
        if hook_type == bstack1lllll_opy_ (u"ࠥࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠣᄚ"):
            return bstack1lllll_opy_ (u"ࠦࡘ࡫ࡴࡶࡲࠣ࡬ࡴࡵ࡫ࠣᄛ")
        elif hook_type == bstack1lllll_opy_ (u"ࠧࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠤᄜ"):
            return bstack1lllll_opy_ (u"ࠨࡔࡦࡣࡵࡨࡴࡽ࡮ࠡࡪࡲࡳࡰࠨᄝ")
    @staticmethod
    def bstack1l11ll111l_opy_(bstack1lllll1ll_opy_):
        try:
            if not bstack1lllll111_opy_.on():
                return bstack1lllll1ll_opy_
            if os.environ.get(bstack1lllll_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡒࡆࡔࡘࡒࠧᄞ"), None) == bstack1lllll_opy_ (u"ࠣࡶࡵࡹࡪࠨᄟ"):
                tests = os.environ.get(bstack1lllll_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔ࡟ࡕࡇࡖࡘࡘࠨᄠ"), None)
                if tests is None or tests == bstack1lllll_opy_ (u"ࠥࡲࡺࡲ࡬ࠣᄡ"):
                    return bstack1lllll1ll_opy_
                bstack1lllll1ll_opy_ = tests.split(bstack1lllll_opy_ (u"ࠫ࠱࠭ᄢ"))
                return bstack1lllll1ll_opy_
        except Exception as exc:
            print(bstack1lllll_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡷ࡫ࡲࡶࡰࠣ࡬ࡦࡴࡤ࡭ࡧࡵ࠾ࠥࠨᄣ"), str(exc))
        return bstack1lllll1ll_opy_