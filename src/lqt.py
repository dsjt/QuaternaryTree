# -*- coding: utf-8 -*-
import logging
import math
import itertools
from qt_cell import QtCell
from aabb import Aabb
from general import get_2d_morton_number
from util import bit_n_most, flatten

logger = logging.getLogger(__name__)

class LQT(object):
    """線形四分木(LinearQuaternaryTree)

    L: 深さ
    W: 考える空間の幅（＝高さ）
    """
    def __init__(self, L, W):
        self.L = L
        self.N = (4**L-1)//3
        self.data = [None for i in range(self.N)]

        self.W = W
        self.U = W / (2**(L-1))

        # 深さごとに空間オブジェクトを用意する
        for l in range(L):
            for morton_order in range(4**l):
                self.data[self.index_from_lm(l, morton_order)] = QtCell(
                    l, morton_order)
        pass

    def index_from_lm(self, l, n):
        """空間分割の深さlと、その空間におけるモートン番号nから、線形配列上の対応箇所へ
        のインデックスを返す
        """
        return (4**l-1)//3 + n

    def lm_from_index(self, i):
        """
        線形配列上のインデックスから、空間分割の深さlとモートン番号nを得る
        """
        l = int(math.log(3*i+1)/math.log(4))
        n = i-(4**l-1)//3
        return l, n

    def register(self, aabb: Aabb):
        """AabbをLQTに登録する。情報を変更した場合も再登録する。
        """
        logger.debug(f"lqt register {aabb}")
        # Aabbが既に空間に登録されている場合、登録を解除する。
        if aabb.cell is not None:
            aabb.cell.remove(aabb)
            aabb.cell = None

        # aabbのモートンオーダを求める
        (x1, y1), (x2, y2) = aabb.get_points()
        mn1 = get_2d_morton_number(int(x1 / self.U), int(y1 / self.U))
        mn2 = get_2d_morton_number(int(x2 / self.U), int(y2 / self.U))

        if mn1 == mn2:
            # モートンオーダが完全に一致する場合は、最下層のmn1(=mn2)に属する。
            l, mn = self.L-1, mn1
        else:
            l, mn = self.common_ancestor(mn1, mn2)

        cell = self.data[self.index_from_lm(l, mn)]
        cell.add(aabb)
        aabb.registered(cell)
        return

    def update(self, aabb: Aabb):
        return self.register(aabb)

    def common_ancestor(self, mn1, mn2):
        """
        モートン番号mn1, mn2の両方が含まれる空間の深さlとモートン番号mnを得る。
        """
        xor_value = mn1 ^ mn2
        # 最上位bitの桁数(0-index)
        n = bit_n_most(xor_value)-1
        # 最下層はself.L-1, そこから(n//2 + 1)上位
        l = self.L-2-n//2
        mn = mn1 >> ((n//2+1)*2)
        return l, mn

    def overlap_pairs(self):
        """
        接触する二つのオブジェクトを返すイテレータ
        """
        stack = [~0, 0]
        candidates = []
        while stack:
            current = stack.pop()
            if current >= 0:
                l, n = self.lm_from_index(current)
                # 未探索
                # まずは現在の空間内のオブジェクト同士の接触を考える
                for obj1, obj2 in itertools.combinations(self.data[current], 2):
                    if obj1.is_overlapped_with(obj2):
                        yield (obj1, obj2)
                # 次に祖先のオブジェクトとの接触を考える
                for obj1 in self.data[current]:
                    for obj2 in flatten(candidates):
                        if obj1.is_overlapped_with(obj2):
                            yield(obj1, obj2)
                # 現在の空間のオブジェクトを追加
                candidates.append(self.data[current])

                # 次の空間への参照を追加
                l, n = self.lm_from_index(current)
                if l < self.L-1:  # 最終層でなければ次を追加
                    for i in range(4):
                        m = (n << 2) | i
                        next_cell = self.index_from_lm(l+1, m)
                        stack.append(~next_cell)
                        stack.append(next_cell)

            else:
                # 探索済み
                candidates.pop()
