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
bstack1l1l1ll11l_opy_ = 10
bstack1l1l1ll111_opy_ = 5
bstack1l1l1l1l1l_opy_ = 30
bstack1l1l1l1lll_opy_ = 2
class bstack1l1l1l11l1_opy_:
    def __init__(self, handler, bstack1l1l1lll1l_opy_=bstack1l1l1ll11l_opy_, bstack1l1l1lll11_opy_=bstack1l1l1ll111_opy_):
        self.queue = []
        self.handler = handler
        self.bstack1l1l1lll1l_opy_ = bstack1l1l1lll1l_opy_
        self.bstack1l1l1lll11_opy_ = bstack1l1l1lll11_opy_
        self.lock = threading.Lock()
        self.timer = None
    def start(self):
        if not self.timer:
            self.bstack1l1l1ll1l1_opy_()
    def bstack1l1l1ll1l1_opy_(self):
        self.timer = threading.Timer(self.bstack1l1l1lll11_opy_, self.bstack1l1l1l1ll1_opy_)
        self.timer.start()
    def bstack1l1l1ll1ll_opy_(self):
        self.timer.cancel()
    def bstack1l1l1l1l11_opy_(self):
        self.bstack1l1l1ll1ll_opy_()
        self.bstack1l1l1ll1l1_opy_()
    def add(self, event):
        with self.lock:
            self.queue.append(event)
            if len(self.queue) >= self.bstack1l1l1lll1l_opy_:
                t = threading.Thread(target=self.bstack1l1l1l1ll1_opy_)
                t.start()
                self.bstack1l1l1l1l11_opy_()
    def bstack1l1l1l1ll1_opy_(self):
        if len(self.queue) <= 0:
            return
        data = self.queue[:self.bstack1l1l1lll1l_opy_]
        del self.queue[:self.bstack1l1l1lll1l_opy_]
        self.handler(data)
    def shutdown(self):
        self.bstack1l1l1ll1ll_opy_()
        while len(self.queue) > 0:
            self.bstack1l1l1l1ll1_opy_()