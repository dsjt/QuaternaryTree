# -*- coding: utf-8 -*-
import logging
logger = logging.getLogger(__name__)

class Aabb(object):
    """
    軸平行な辺を持つ長方形オブジェクト
    """
    def __init__(self, p1, p2):
        # 正規化しながら保存する
        self.p1 = [min(p1[0], p2[0]), min(p1[1], p2[1])]
        self.p2 = [max(p1[0], p2[0]), max(p1[1], p2[1])]

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

    def __repr__(self):
        return f"<Aabb {self.p1=}, {self.p2=}>"

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
        if self.including_point(other.p1):
            return True
        if self.including_point(other.p2):
            return True
        if other.including_point(self.p1):
            return True
        if other.including_point(self.p2):
            return True
        return False
