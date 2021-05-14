# -*- coding: utf-8 -*-
import matplotlib
import matplotlib.pyplot as plt
import logging
logger = logging.getLogger(__name__)

class Aabb(object):
    """
    軸平行な辺を持つ長方形オブジェクト
    """
    def __init__(self, p1, p2, identifier=None):
        # 正規化しながら保存する
        self.p1 = [min(p1[0], p2[0]), min(p1[1], p2[1])]
        self.p2 = [max(p1[0], p2[0]), max(p1[1], p2[1])]

        # 識別子
        self.identifier=identifier

        # 所属する空間
        self.cell = None
        return

    def registered(self, cell):
        """登録される空間を保持する。
        """
        self.cell = cell
        return

    def update(self, p1, p2):
        """位置を更新する。
        """
        self.p1 = p1
        self.p2 = p2
        self.cell.remove(self)
        self.cell = None
        return

    def get_points(self):
        return self.p1, self.p2

    def get_four_points(self):
        p3 = [self.p1[0], self.p2[1]]
        p4 = [self.p2[0], self.p2[1]]
        return self.p1, p3, self.p2, p4

    def __repr__(self):
        return f"<Aabb name={self.identifier} ({self.p1[0]:.3f}, {self.p1[1]:.3f}), ({self.p2[0]:.3f}, {self.p2[1]:.3f})>"

    def including_point(self, point: list[int]):
        """
        点を含んでいるかどうかを判定する
        """
        flag = self.p1[0] <= point[0] < self.p2[0]
        flag &= self.p1[1] <= point[1] < self.p2[1]
        return flag

    def is_overlapped_with(self, other):
        """2つのAabbが重なっているかどうかを判定する
        """
        if (self.p2[0] > other.p1[0]) \
           and (self.p1[0] < other.p2[0]) \
           and (self.p2[1] > other.p1[1]) \
           and (self.p1[1] < other.p2[1]):
            return True
        if (other.p2[0] > self.p1[0]) \
           and (other.p1[0] < self.p2[0]) \
           and (other.p2[1] > self.p1[1]) \
           and (other.p1[1] < self.p2[1]):
            return True
        return False

    def plot(self, ax, **kwargs):
        w = self.p2[0]-self.p1[0]
        h = self.p2[1]-self.p1[1]
        r = matplotlib.patches.Rectangle(xy=self.p1, width=w, height=h,
                                         ec='red', linestyle="-", fill=False)
        ax.add_patch(r)

        if self.identifier is not None:
            ax.annotate(self.identifier, xy=self.p1)
        return
