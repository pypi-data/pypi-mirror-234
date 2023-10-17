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
import os
import re
import subprocess
from urllib.parse import urlparse
import git
import requests
from packaging import version
from bstack_utils.config import Config
from bstack_utils.constants import bstack1ll111ll1l_opy_, bstack1111l1l1l_opy_, bstack11111111l_opy_, bstack1llll1l1_opy_
from bstack_utils.messages import bstack1l1lll1l1_opy_
from bstack_utils.proxy import bstack111ll1111_opy_
bstack1l1l1l1l1_opy_ = Config.get_instance()
def bstack1ll11111l1_opy_(config):
    return config[bstack1lllll_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ༃")]
def bstack1l1ll1ll1l_opy_(config):
    return config[bstack1lllll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ༄")]
def bstack1l1llll1ll_opy_(obj):
    values = []
    bstack1ll1111lll_opy_ = re.compile(bstack1lllll_opy_ (u"ࡴࠥࡢࡈ࡛ࡓࡕࡑࡐࡣ࡙ࡇࡇࡠ࡞ࡧ࠯ࠩࠨ༅"), re.I)
    for key in obj.keys():
        if bstack1ll1111lll_opy_.match(key):
            values.append(obj[key])
    return values
def bstack1l1lllll11_opy_(config):
    tags = []
    tag = config.get(bstack1lllll_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯ࡗࡥ࡬ࠨ༆")) or os.environ.get(bstack1lllll_opy_ (u"ࠦࡈ࡛ࡓࡕࡑࡐࡣ࡙ࡇࡇࠣ༇"))
    if tag:
        tags.append(tag)
    tags.extend(bstack1l1llll1ll_opy_(os.environ))
    tags.extend(bstack1l1llll1ll_opy_(config))
    return tags
def bstack1ll1111ll1_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack1l1lll1ll1_opy_(bstack1ll1111l11_opy_):
    if not bstack1ll1111l11_opy_:
        return bstack1lllll_opy_ (u"ࠬ࠭༈")
    return bstack1lllll_opy_ (u"ࠨࡻࡾࠢࠫࡿࢂ࠯ࠢ༉").format(bstack1ll1111l11_opy_.name, bstack1ll1111l11_opy_.email)
def bstack1l1lll1l11_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack1l1ll1ll11_opy_ = repo.common_dir
        info = {
            bstack1lllll_opy_ (u"ࠢࡴࡪࡤࠦ༊"): repo.head.commit.hexsha,
            bstack1lllll_opy_ (u"ࠣࡵ࡫ࡳࡷࡺ࡟ࡴࡪࡤࠦ་"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack1lllll_opy_ (u"ࠤࡥࡶࡦࡴࡣࡩࠤ༌"): repo.active_branch.name,
            bstack1lllll_opy_ (u"ࠥࡸࡦ࡭ࠢ།"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack1lllll_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡸࡪࡸࠢ༎"): bstack1l1lll1ll1_opy_(repo.head.commit.committer),
            bstack1lllll_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡹ࡫ࡲࡠࡦࡤࡸࡪࠨ༏"): repo.head.commit.committed_datetime.isoformat(),
            bstack1lllll_opy_ (u"ࠨࡡࡶࡶ࡫ࡳࡷࠨ༐"): bstack1l1lll1ll1_opy_(repo.head.commit.author),
            bstack1lllll_opy_ (u"ࠢࡢࡷࡷ࡬ࡴࡸ࡟ࡥࡣࡷࡩࠧ༑"): repo.head.commit.authored_datetime.isoformat(),
            bstack1lllll_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡠ࡯ࡨࡷࡸࡧࡧࡦࠤ༒"): repo.head.commit.message,
            bstack1lllll_opy_ (u"ࠤࡵࡳࡴࡺࠢ༓"): repo.git.rev_parse(bstack1lllll_opy_ (u"ࠥ࠱࠲ࡹࡨࡰࡹ࠰ࡸࡴࡶ࡬ࡦࡸࡨࡰࠧ༔")),
            bstack1lllll_opy_ (u"ࠦࡨࡵ࡭࡮ࡱࡱࡣ࡬࡯ࡴࡠࡦ࡬ࡶࠧ༕"): bstack1l1ll1ll11_opy_,
            bstack1lllll_opy_ (u"ࠧࡽ࡯ࡳ࡭ࡷࡶࡪ࡫࡟ࡨ࡫ࡷࡣࡩ࡯ࡲࠣ༖"): subprocess.check_output([bstack1lllll_opy_ (u"ࠨࡧࡪࡶࠥ༗"), bstack1lllll_opy_ (u"ࠢࡳࡧࡹ࠱ࡵࡧࡲࡴࡧ༘ࠥ"), bstack1lllll_opy_ (u"ࠣ࠯࠰࡫࡮ࡺ࠭ࡤࡱࡰࡱࡴࡴ࠭ࡥ࡫ࡵ༙ࠦ")]).strip().decode(
                bstack1lllll_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨ༚")),
            bstack1lllll_opy_ (u"ࠥࡰࡦࡹࡴࡠࡶࡤ࡫ࠧ༛"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack1lllll_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡷࡤࡹࡩ࡯ࡥࡨࡣࡱࡧࡳࡵࡡࡷࡥ࡬ࠨ༜"): repo.git.rev_list(
                bstack1lllll_opy_ (u"ࠧࢁࡽ࠯࠰ࡾࢁࠧ༝").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack1ll111l11l_opy_ = []
        for remote in remotes:
            bstack1ll111l111_opy_ = {
                bstack1lllll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ༞"): remote.name,
                bstack1lllll_opy_ (u"ࠢࡶࡴ࡯ࠦ༟"): remote.url,
            }
            bstack1ll111l11l_opy_.append(bstack1ll111l111_opy_)
        return {
            bstack1lllll_opy_ (u"ࠣࡰࡤࡱࡪࠨ༠"): bstack1lllll_opy_ (u"ࠤࡪ࡭ࡹࠨ༡"),
            **info,
            bstack1lllll_opy_ (u"ࠥࡶࡪࡳ࡯ࡵࡧࡶࠦ༢"): bstack1ll111l11l_opy_
        }
    except Exception as err:
        print(bstack1lllll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡴࡶࡵ࡭ࡣࡷ࡭ࡳ࡭ࠠࡈ࡫ࡷࠤࡲ࡫ࡴࡢࡦࡤࡸࡦࠦࡷࡪࡶ࡫ࠤࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠢ༣").format(err))
        return {}
def bstack1l1lll1111_opy_():
    env = os.environ
    if (bstack1lllll_opy_ (u"ࠧࡐࡅࡏࡍࡌࡒࡘࡥࡕࡓࡎࠥ༤") in env and len(env[bstack1lllll_opy_ (u"ࠨࡊࡆࡐࡎࡍࡓ࡙࡟ࡖࡔࡏࠦ༥")]) > 0) or (
            bstack1lllll_opy_ (u"ࠢࡋࡇࡑࡏࡎࡔࡓࡠࡊࡒࡑࡊࠨ༦") in env and len(env[bstack1lllll_opy_ (u"ࠣࡌࡈࡒࡐࡏࡎࡔࡡࡋࡓࡒࡋࠢ༧")]) > 0):
        return {
            bstack1lllll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ༨"): bstack1lllll_opy_ (u"ࠥࡎࡪࡴ࡫ࡪࡰࡶࠦ༩"),
            bstack1lllll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ༪"): env.get(bstack1lllll_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣ༫")),
            bstack1lllll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ༬"): env.get(bstack1lllll_opy_ (u"ࠢࡋࡑࡅࡣࡓࡇࡍࡆࠤ༭")),
            bstack1lllll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ༮"): env.get(bstack1lllll_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣ༯"))
        }
    if env.get(bstack1lllll_opy_ (u"ࠥࡇࡎࠨ༰")) == bstack1lllll_opy_ (u"ࠦࡹࡸࡵࡦࠤ༱") and env.get(bstack1lllll_opy_ (u"ࠧࡉࡉࡓࡅࡏࡉࡈࡏࠢ༲")) == bstack1lllll_opy_ (u"ࠨࡴࡳࡷࡨࠦ༳"):
        return {
            bstack1lllll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ༴"): bstack1lllll_opy_ (u"ࠣࡅ࡬ࡶࡨࡲࡥࡄࡋ༵ࠥ"),
            bstack1lllll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ༶"): env.get(bstack1lllll_opy_ (u"ࠥࡇࡎࡘࡃࡍࡇࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨ༷")),
            bstack1lllll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ༸"): env.get(bstack1lllll_opy_ (u"ࠧࡉࡉࡓࡅࡏࡉࡤࡐࡏࡃࠤ༹")),
            bstack1lllll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ༺"): env.get(bstack1lllll_opy_ (u"ࠢࡄࡋࡕࡇࡑࡋ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࠥ༻"))
        }
    if env.get(bstack1lllll_opy_ (u"ࠣࡅࡌࠦ༼")) == bstack1lllll_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ༽") and env.get(bstack1lllll_opy_ (u"ࠥࡘࡗࡇࡖࡊࡕࠥ༾")) == bstack1lllll_opy_ (u"ࠦࡹࡸࡵࡦࠤ༿"):
        return {
            bstack1lllll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥཀ"): bstack1lllll_opy_ (u"ࠨࡔࡳࡣࡹ࡭ࡸࠦࡃࡊࠤཁ"),
            bstack1lllll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥག"): env.get(bstack1lllll_opy_ (u"ࠣࡖࡕࡅ࡛ࡏࡓࡠࡄࡘࡍࡑࡊ࡟ࡘࡇࡅࡣ࡚ࡘࡌࠣགྷ")),
            bstack1lllll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦང"): env.get(bstack1lllll_opy_ (u"ࠥࡘࡗࡇࡖࡊࡕࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧཅ")),
            bstack1lllll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥཆ"): env.get(bstack1lllll_opy_ (u"࡚ࠧࡒࡂࡘࡌࡗࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦཇ"))
        }
    if env.get(bstack1lllll_opy_ (u"ࠨࡃࡊࠤ཈")) == bstack1lllll_opy_ (u"ࠢࡵࡴࡸࡩࠧཉ") and env.get(bstack1lllll_opy_ (u"ࠣࡅࡌࡣࡓࡇࡍࡆࠤཊ")) == bstack1lllll_opy_ (u"ࠤࡦࡳࡩ࡫ࡳࡩ࡫ࡳࠦཋ"):
        return {
            bstack1lllll_opy_ (u"ࠥࡲࡦࡳࡥࠣཌ"): bstack1lllll_opy_ (u"ࠦࡈࡵࡤࡦࡵ࡫࡭ࡵࠨཌྷ"),
            bstack1lllll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣཎ"): None,
            bstack1lllll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣཏ"): None,
            bstack1lllll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨཐ"): None
        }
    if env.get(bstack1lllll_opy_ (u"ࠣࡄࡌࡘࡇ࡛ࡃࡌࡇࡗࡣࡇࡘࡁࡏࡅࡋࠦད")) and env.get(bstack1lllll_opy_ (u"ࠤࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡉࡏࡎࡏࡌࡘࠧདྷ")):
        return {
            bstack1lllll_opy_ (u"ࠥࡲࡦࡳࡥࠣན"): bstack1lllll_opy_ (u"ࠦࡇ࡯ࡴࡣࡷࡦ࡯ࡪࡺࠢཔ"),
            bstack1lllll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣཕ"): env.get(bstack1lllll_opy_ (u"ࠨࡂࡊࡖࡅ࡙ࡈࡑࡅࡕࡡࡊࡍ࡙ࡥࡈࡕࡖࡓࡣࡔࡘࡉࡈࡋࡑࠦབ")),
            bstack1lllll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤབྷ"): None,
            bstack1lllll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢམ"): env.get(bstack1lllll_opy_ (u"ࠤࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦཙ"))
        }
    if env.get(bstack1lllll_opy_ (u"ࠥࡇࡎࠨཚ")) == bstack1lllll_opy_ (u"ࠦࡹࡸࡵࡦࠤཛ") and env.get(bstack1lllll_opy_ (u"ࠧࡊࡒࡐࡐࡈࠦཛྷ")) == bstack1lllll_opy_ (u"ࠨࡴࡳࡷࡨࠦཝ"):
        return {
            bstack1lllll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧཞ"): bstack1lllll_opy_ (u"ࠣࡆࡵࡳࡳ࡫ࠢཟ"),
            bstack1lllll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧའ"): env.get(bstack1lllll_opy_ (u"ࠥࡈࡗࡕࡎࡆࡡࡅ࡙ࡎࡒࡄࡠࡎࡌࡒࡐࠨཡ")),
            bstack1lllll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨར"): None,
            bstack1lllll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦལ"): env.get(bstack1lllll_opy_ (u"ࠨࡄࡓࡑࡑࡉࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦཤ"))
        }
    if env.get(bstack1lllll_opy_ (u"ࠢࡄࡋࠥཥ")) == bstack1lllll_opy_ (u"ࠣࡶࡵࡹࡪࠨས") and env.get(bstack1lllll_opy_ (u"ࠤࡖࡉࡒࡇࡐࡉࡑࡕࡉࠧཧ")) == bstack1lllll_opy_ (u"ࠥࡸࡷࡻࡥࠣཨ"):
        return {
            bstack1lllll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤཀྵ"): bstack1lllll_opy_ (u"࡙ࠧࡥ࡮ࡣࡳ࡬ࡴࡸࡥࠣཪ"),
            bstack1lllll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤཫ"): env.get(bstack1lllll_opy_ (u"ࠢࡔࡇࡐࡅࡕࡎࡏࡓࡇࡢࡓࡗࡍࡁࡏࡋ࡝ࡅ࡙ࡏࡏࡏࡡࡘࡖࡑࠨཬ")),
            bstack1lllll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ཭"): env.get(bstack1lllll_opy_ (u"ࠤࡖࡉࡒࡇࡐࡉࡑࡕࡉࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢ཮")),
            bstack1lllll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ཯"): env.get(bstack1lllll_opy_ (u"ࠦࡘࡋࡍࡂࡒࡋࡓࡗࡋ࡟ࡋࡑࡅࡣࡎࡊࠢ཰"))
        }
    if env.get(bstack1lllll_opy_ (u"ࠧࡉࡉཱࠣ")) == bstack1lllll_opy_ (u"ࠨࡴࡳࡷࡨིࠦ") and env.get(bstack1lllll_opy_ (u"ࠢࡈࡋࡗࡐࡆࡈ࡟ࡄࡋཱིࠥ")) == bstack1lllll_opy_ (u"ࠣࡶࡵࡹࡪࠨུ"):
        return {
            bstack1lllll_opy_ (u"ࠤࡱࡥࡲ࡫ཱུࠢ"): bstack1lllll_opy_ (u"ࠥࡋ࡮ࡺࡌࡢࡤࠥྲྀ"),
            bstack1lllll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢཷ"): env.get(bstack1lllll_opy_ (u"ࠧࡉࡉࡠࡌࡒࡆࡤ࡛ࡒࡍࠤླྀ")),
            bstack1lllll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣཹ"): env.get(bstack1lllll_opy_ (u"ࠢࡄࡋࡢࡎࡔࡈ࡟ࡏࡃࡐࡉེࠧ")),
            bstack1lllll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸཻࠢ"): env.get(bstack1lllll_opy_ (u"ࠤࡆࡍࡤࡐࡏࡃࡡࡌࡈོࠧ"))
        }
    if env.get(bstack1lllll_opy_ (u"ࠥࡇࡎࠨཽ")) == bstack1lllll_opy_ (u"ࠦࡹࡸࡵࡦࠤཾ") and env.get(bstack1lllll_opy_ (u"ࠧࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࠣཿ")) == bstack1lllll_opy_ (u"ࠨࡴࡳࡷࡨྀࠦ"):
        return {
            bstack1lllll_opy_ (u"ࠢ࡯ࡣࡰࡩཱྀࠧ"): bstack1lllll_opy_ (u"ࠣࡄࡸ࡭ࡱࡪ࡫ࡪࡶࡨࠦྂ"),
            bstack1lllll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧྃ"): env.get(bstack1lllll_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡍࡌࡘࡊࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤ྄")),
            bstack1lllll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ྅"): env.get(bstack1lllll_opy_ (u"ࠧࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࡠࡎࡄࡆࡊࡒࠢ྆")) or env.get(bstack1lllll_opy_ (u"ࠨࡂࡖࡋࡏࡈࡐࡏࡔࡆࡡࡓࡍࡕࡋࡌࡊࡐࡈࡣࡓࡇࡍࡆࠤ྇")),
            bstack1lllll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨྈ"): env.get(bstack1lllll_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥྉ"))
        }
    if env.get(bstack1lllll_opy_ (u"ࠤࡗࡊࡤࡈࡕࡊࡎࡇࠦྊ")) == bstack1lllll_opy_ (u"ࠥࡘࡷࡻࡥࠣྋ"):
        return {
            bstack1lllll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤྌ"): bstack1lllll_opy_ (u"ࠧ࡜ࡩࡴࡷࡤࡰ࡙ࠥࡴࡶࡦ࡬ࡳ࡚ࠥࡥࡢ࡯ࠣࡗࡪࡸࡶࡪࡥࡨࡷࠧྍ"),
            bstack1lllll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤྎ"): bstack1l1ll1l1ll_opy_ (u"ࠢࡼࡧࡱࡺ࠳࡭ࡥࡵࠪࠪࡗ࡞࡙ࡔࡆࡏࡢࡘࡊࡇࡍࡇࡑࡘࡒࡉࡇࡔࡊࡑࡑࡗࡊࡘࡖࡆࡔࡘࡖࡎ࠭ࠩࡾࡽࡨࡲࡻ࠴ࡧࡦࡶࠫࠫࡘ࡟ࡓࡕࡇࡐࡣ࡙ࡋࡁࡎࡒࡕࡓࡏࡋࡃࡕࡋࡇࠫ࠮ࢃࠢྏ"),
            bstack1lllll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥྐ"): env.get(bstack1lllll_opy_ (u"ࠤࡖ࡝ࡘ࡚ࡅࡎࡡࡇࡉࡋࡏࡎࡊࡖࡌࡓࡓࡏࡄࠣྑ")),
            bstack1lllll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤྒ"): env.get(bstack1lllll_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡋࡇࠦྒྷ"))
        }
    return {bstack1lllll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦྔ"): None}
def get_host_info():
    uname = os.uname()
    return {
        bstack1lllll_opy_ (u"ࠨࡨࡰࡵࡷࡲࡦࡳࡥࠣྕ"): uname.nodename,
        bstack1lllll_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠤྖ"): uname.sysname,
        bstack1lllll_opy_ (u"ࠣࡶࡼࡴࡪࠨྗ"): uname.machine,
        bstack1lllll_opy_ (u"ࠤࡹࡩࡷࡹࡩࡰࡰࠥ྘"): uname.version,
        bstack1lllll_opy_ (u"ࠥࡥࡷࡩࡨࠣྙ"): uname.machine
    }
def bstack1l1ll1llll_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack1l1lllllll_opy_():
    if bstack1l1l1l1l1_opy_.get_property(bstack1lllll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠬྚ")):
        return bstack1lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫྛ")
    return bstack1lllll_opy_ (u"࠭ࡵ࡯࡭ࡱࡳࡼࡴ࡟ࡨࡴ࡬ࡨࠬྜ")
def bstack1l1llll111_opy_(driver):
    info = {
        bstack1lllll_opy_ (u"ࠧࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ྜྷ"): driver.capabilities,
        bstack1lllll_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠬྞ"): driver.session_id,
        bstack1lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪྟ"): driver.capabilities.get(bstack1lllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨྠ"), None),
        bstack1lllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ྡ"): driver.capabilities.get(bstack1lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ྡྷ"), None),
        bstack1lllll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠨྣ"): driver.capabilities.get(bstack1lllll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪ࠭ྤ"), None),
    }
    if bstack1l1lllllll_opy_() == bstack1lllll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧྥ"):
        info[bstack1lllll_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࠪྦ")] = bstack1lllll_opy_ (u"ࠪࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦࠩྦྷ") if bstack11lll11ll_opy_() else bstack1lllll_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭ྨ")
    return info
def bstack11lll11ll_opy_():
    if bstack1l1l1l1l1_opy_.get_property(bstack1lllll_opy_ (u"ࠬࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠫྩ")):
        return True
    if bstack1ll111ll11_opy_(os.environ.get(bstack1lllll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧྪ"), None)):
        return True
    return False
def bstack1l11ll1ll_opy_(bstack1ll111l1l1_opy_, url, data, config):
    headers = config.get(bstack1lllll_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨྫ"), None)
    proxies = bstack111ll1111_opy_(config, url)
    auth = config.get(bstack1lllll_opy_ (u"ࠨࡣࡸࡸ࡭࠭ྫྷ"), None)
    response = requests.request(
            bstack1ll111l1l1_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    return response
def bstack11111l11l_opy_(bstack1l111l1ll_opy_, size):
    bstack1l111ll11_opy_ = []
    while len(bstack1l111l1ll_opy_) > size:
        bstack111lll11_opy_ = bstack1l111l1ll_opy_[:size]
        bstack1l111ll11_opy_.append(bstack111lll11_opy_)
        bstack1l111l1ll_opy_ = bstack1l111l1ll_opy_[size:]
    bstack1l111ll11_opy_.append(bstack1l111l1ll_opy_)
    return bstack1l111ll11_opy_
def bstack1l1ll1lll1_opy_(message):
    os.write(1, bytes(message, bstack1lllll_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨྭ")))
    os.write(1, bytes(bstack1lllll_opy_ (u"ࠪࡠࡳ࠭ྮ"), bstack1lllll_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪྯ")))
def bstack1l1lll111l_opy_():
    return os.environ[bstack1lllll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨྰ")].lower() == bstack1lllll_opy_ (u"࠭ࡴࡳࡷࡨࠫྱ")
def bstack11ll1l1ll_opy_(bstack1l1lll1lll_opy_):
    return bstack1lllll_opy_ (u"ࠧࡼࡿ࠲ࡿࢂ࠭ྲ").format(bstack1ll111ll1l_opy_, bstack1l1lll1lll_opy_)
def bstack11l11l1l_opy_():
    return datetime.datetime.utcnow().isoformat() + bstack1lllll_opy_ (u"ࠨ࡜ࠪླ")
def bstack1l1lllll1l_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack1lllll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩྴ")
    else:
        return bstack1lllll_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪྵ")
def bstack1ll111ll11_opy_(val):
    return val.__str__().lower() == bstack1lllll_opy_ (u"ࠫࡹࡸࡵࡦࠩྶ")
def bstack1l1lll1l1l_opy_(val):
    return val.__str__().lower() == bstack1lllll_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫྷ")
def bstack1l1llllll1_opy_(bstack1l1llll11l_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack1l1llll11l_opy_ as e:
                print(bstack1lllll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࡼࡿࠣ࠱ࡃࠦࡻࡾ࠼ࠣࡿࢂࠨྸ").format(func.__name__, bstack1l1llll11l_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack1ll111l1ll_opy_(bstack1l1llll1l1_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack1l1llll1l1_opy_(cls, *args, **kwargs)
            except bstack1l1llll11l_opy_ as e:
                print(bstack1lllll_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠡࡽࢀࠤ࠲ࡄࠠࡼࡿ࠽ࠤࢀࢃࠢྐྵ").format(bstack1l1llll1l1_opy_.__name__, bstack1l1llll11l_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack1ll111l1ll_opy_
    else:
        return decorator
def bstack1l1111l1l_opy_(bstack1ll1l11111_opy_):
    if bstack1lllll_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬྺ") in bstack1ll1l11111_opy_ and bstack1l1lll1l1l_opy_(bstack1ll1l11111_opy_[bstack1lllll_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ྻ")]):
        return False
    if bstack1lllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬྼ") in bstack1ll1l11111_opy_ and bstack1l1lll1l1l_opy_(bstack1ll1l11111_opy_[bstack1lllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭྽")]):
        return False
    return True
def bstack1l1lll11l1_opy_():
    try:
        from pytest_bdd import reporting
        return True
    except Exception as e:
        return False
def bstack1lllll1lll_opy_(hub_url):
    if bstack11ll1l1l1_opy_() <= version.parse(bstack1lllll_opy_ (u"ࠬ࠹࠮࠲࠵࠱࠴ࠬ྾")):
        if hub_url != bstack1lllll_opy_ (u"࠭ࠧ྿"):
            return bstack1lllll_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣ࿀") + hub_url + bstack1lllll_opy_ (u"ࠣ࠼࠻࠴࠴ࡽࡤ࠰ࡪࡸࡦࠧ࿁")
        return bstack11111111l_opy_
    if hub_url != bstack1lllll_opy_ (u"ࠩࠪ࿂"):
        return bstack1lllll_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧ࿃") + hub_url + bstack1lllll_opy_ (u"ࠦ࠴ࡽࡤ࠰ࡪࡸࡦࠧ࿄")
    return bstack1llll1l1_opy_
def bstack1l1lll11ll_opy_():
    return isinstance(os.getenv(bstack1lllll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕ࡟ࡔࡆࡕࡗࡣࡕࡒࡕࡈࡋࡑࠫ࿅")), str)
def bstack111lll11l_opy_(url):
    return urlparse(url).hostname
def bstack1llll1lll1_opy_(hostname):
    for bstack1l1l1l1ll_opy_ in bstack1111l1l1l_opy_:
        regex = re.compile(bstack1l1l1l1ll_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack1ll111111l_opy_(bstack1ll1111l1l_opy_, file_name, logger):
    bstack11111111_opy_ = os.path.join(os.path.expanduser(bstack1lllll_opy_ (u"࠭ࡾࠨ࿆")), bstack1ll1111l1l_opy_)
    try:
        if not os.path.exists(bstack11111111_opy_):
            os.makedirs(bstack11111111_opy_)
        file_path = os.path.join(os.path.expanduser(bstack1lllll_opy_ (u"ࠧࡿࠩ࿇")), bstack1ll1111l1l_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack1lllll_opy_ (u"ࠨࡹࠪ࿈")):
                pass
            with open(file_path, bstack1lllll_opy_ (u"ࠤࡺ࠯ࠧ࿉")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack1l1lll1l1_opy_.format(str(e)))
def bstack1ll11111ll_opy_(file_name, key, value, logger):
    file_path = bstack1ll111111l_opy_(bstack1lllll_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪ࿊"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack1ll111l1l_opy_ = json.load(open(file_path, bstack1lllll_opy_ (u"ࠫࡷࡨࠧ࿋")))
        else:
            bstack1ll111l1l_opy_ = {}
        bstack1ll111l1l_opy_[key] = value
        with open(file_path, bstack1lllll_opy_ (u"ࠧࡽࠫࠣ࿌")) as outfile:
            json.dump(bstack1ll111l1l_opy_, outfile)
def bstack1llll111ll_opy_(file_name, logger):
    file_path = bstack1ll111111l_opy_(bstack1lllll_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭࿍"), file_name, logger)
    bstack1ll111l1l_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack1lllll_opy_ (u"ࠧࡳࠩ࿎")) as bstack1l1l11111_opy_:
            bstack1ll111l1l_opy_ = json.load(bstack1l1l11111_opy_)
    return bstack1ll111l1l_opy_
def bstack1l11lll1l_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack1lllll_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡨࡪࡲࡥࡵ࡫ࡱ࡫ࠥ࡬ࡩ࡭ࡧ࠽ࠤࠬ࿏") + file_path + bstack1lllll_opy_ (u"ࠩࠣࠫ࿐") + str(e))
def bstack11ll1l1l1_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack1lllll_opy_ (u"ࠥࡀࡓࡕࡔࡔࡇࡗࡂࠧ࿑")
def bstack1l11l1111_opy_(config):
    if bstack1lllll_opy_ (u"ࠫ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪ࿒") in config:
        del (config[bstack1lllll_opy_ (u"ࠬ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫ࿓")])
        return False
    if bstack11ll1l1l1_opy_() < version.parse(bstack1lllll_opy_ (u"࠭࠳࠯࠶࠱࠴ࠬ࿔")):
        return False
    if bstack11ll1l1l1_opy_() >= version.parse(bstack1lllll_opy_ (u"ࠧ࠵࠰࠴࠲࠺࠭࿕")):
        return True
    if bstack1lllll_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨ࿖") in config and config[bstack1lllll_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩ࿗")] is False:
        return False
    else:
        return True
def bstack1l111l111_opy_(args_list, bstack1ll1111111_opy_):
    index = -1
    for value in bstack1ll1111111_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index