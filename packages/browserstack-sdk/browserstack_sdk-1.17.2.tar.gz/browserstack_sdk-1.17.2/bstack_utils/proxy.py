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
import os
from urllib.parse import urlparse
from bstack_utils.messages import bstack1l1ll11lll_opy_
def bstack1l1ll111l1_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack1l1ll11111_opy_(bstack1l1l1lllll_opy_, bstack1l1ll11l11_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack1l1l1lllll_opy_):
        with open(bstack1l1l1lllll_opy_) as f:
            pac = PACFile(f.read())
    elif bstack1l1ll111l1_opy_(bstack1l1l1lllll_opy_):
        pac = get_pac(url=bstack1l1l1lllll_opy_)
    else:
        raise Exception(bstack1lllll_opy_ (u"ࠩࡓࡥࡨࠦࡦࡪ࡮ࡨࠤࡩࡵࡥࡴࠢࡱࡳࡹࠦࡥࡹ࡫ࡶࡸ࠿ࠦࡻࡾࠩဝ").format(bstack1l1l1lllll_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack1lllll_opy_ (u"ࠥ࠼࠳࠾࠮࠹࠰࠻ࠦသ"), 80))
        bstack1l1ll1111l_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack1l1ll1111l_opy_ = bstack1lllll_opy_ (u"ࠫ࠵࠴࠰࠯࠲࠱࠴ࠬဟ")
    proxy_url = session.get_pac().find_proxy_for_url(bstack1l1ll11l11_opy_, bstack1l1ll1111l_opy_)
    return proxy_url
def bstack1l111lll1_opy_(config):
    return bstack1lllll_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨဠ") in config or bstack1lllll_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪအ") in config
def bstack1l1l111l1_opy_(config):
    if not bstack1l111lll1_opy_(config):
        return
    if config.get(bstack1lllll_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪဢ")):
        return config.get(bstack1lllll_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫဣ"))
    if config.get(bstack1lllll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ဤ")):
        return config.get(bstack1lllll_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧဥ"))
def bstack111ll1111_opy_(config, bstack1l1ll11l11_opy_):
    proxy = bstack1l1l111l1_opy_(config)
    proxies = {}
    if config.get(bstack1lllll_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧဦ")) or config.get(bstack1lllll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩဧ")):
        if proxy.endswith(bstack1lllll_opy_ (u"࠭࠮ࡱࡣࡦࠫဨ")):
            proxies = bstack1ll1ll1111_opy_(proxy, bstack1l1ll11l11_opy_)
        else:
            proxies = {
                bstack1lllll_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭ဩ"): proxy
            }
    return proxies
def bstack1ll1ll1111_opy_(bstack1l1l1lllll_opy_, bstack1l1ll11l11_opy_):
    proxies = {}
    global bstack1l1l1llll1_opy_
    if bstack1lllll_opy_ (u"ࠨࡒࡄࡇࡤࡖࡒࡐ࡚࡜ࠫဪ") in globals():
        return bstack1l1l1llll1_opy_
    try:
        proxy = bstack1l1ll11111_opy_(bstack1l1l1lllll_opy_, bstack1l1ll11l11_opy_)
        if bstack1lllll_opy_ (u"ࠤࡇࡍࡗࡋࡃࡕࠤါ") in proxy:
            proxies = {}
        elif bstack1lllll_opy_ (u"ࠥࡌ࡙࡚ࡐࠣာ") in proxy or bstack1lllll_opy_ (u"ࠦࡍ࡚ࡔࡑࡕࠥိ") in proxy or bstack1lllll_opy_ (u"࡙ࠧࡏࡄࡍࡖࠦီ") in proxy:
            bstack1l1ll111ll_opy_ = proxy.split(bstack1lllll_opy_ (u"ࠨࠠࠣု"))
            if bstack1lllll_opy_ (u"ࠢ࠻࠱࠲ࠦူ") in bstack1lllll_opy_ (u"ࠣࠤေ").join(bstack1l1ll111ll_opy_[1:]):
                proxies = {
                    bstack1lllll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨဲ"): bstack1lllll_opy_ (u"ࠥࠦဳ").join(bstack1l1ll111ll_opy_[1:])
                }
            else:
                proxies = {
                    bstack1lllll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪဴ"): str(bstack1l1ll111ll_opy_[0]).lower() + bstack1lllll_opy_ (u"ࠧࡀ࠯࠰ࠤဵ") + bstack1lllll_opy_ (u"ࠨࠢံ").join(bstack1l1ll111ll_opy_[1:])
                }
        elif bstack1lllll_opy_ (u"ࠢࡑࡔࡒ࡜࡞ࠨ့") in proxy:
            bstack1l1ll111ll_opy_ = proxy.split(bstack1lllll_opy_ (u"ࠣࠢࠥး"))
            if bstack1lllll_opy_ (u"ࠤ࠽࠳࠴ࠨ္") in bstack1lllll_opy_ (u"်ࠥࠦ").join(bstack1l1ll111ll_opy_[1:]):
                proxies = {
                    bstack1lllll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪျ"): bstack1lllll_opy_ (u"ࠧࠨြ").join(bstack1l1ll111ll_opy_[1:])
                }
            else:
                proxies = {
                    bstack1lllll_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬွ"): bstack1lllll_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣှ") + bstack1lllll_opy_ (u"ࠣࠤဿ").join(bstack1l1ll111ll_opy_[1:])
                }
        else:
            proxies = {
                bstack1lllll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨ၀"): proxy
            }
    except Exception as e:
        print(bstack1lllll_opy_ (u"ࠥࡷࡴࡳࡥࠡࡧࡵࡶࡴࡸࠢ၁"), bstack1l1ll11lll_opy_.format(bstack1l1l1lllll_opy_, str(e)))
    bstack1l1l1llll1_opy_ = proxies
    return proxies