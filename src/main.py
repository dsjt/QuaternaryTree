# -*- coding: utf-8 -*-
# 四分木による接触判定を作成する。
# 理論については次を参照: http://marupeke296.com/COL_2D_No8_QuadTree.html
# 実装はいくつかの点で異なるため注意
# - 双方向リストではなくsetを使っている
# - 非再帰DFSは競プロテクを採用
import logging
import random
from aabb import Aabb
from util import AutoSaveFigure
from lqt import LQT
from general import display_aabbs, random_aabb


logging.basicConfig()
logging_levels = {
    "aabb": logging.DEBUG,
    "lqt": logging.DEBUG
}

for mn, level in logging_levels.items():
    logging.getLogger(mn).setLevel(level)

logger = logging.getLogger(__name__)
random.seed(1)

def main():

    with AutoSaveFigure("sample/tmp.png") as fig:
        ax = fig.add_subplot(1, 1, 1)

        # 一辺100の空間にAabbを4つ用意。四分木に追加
        # 4層の四分木を構成し追加
        lqt = LQT(4, 100)

        aabbs = [random_aabb(100, 100, f"{i}") for i in range(4)]
        for aabb in aabbs:
            lqt.register(aabb)

        display_aabbs(100, 100, aabbs, ax)

        # lqtで接触しているオブジェクトを列挙する
        for x1, x2 in lqt.overlap_pairs():
            print(f"Contact {x1} and {x2}")


if __name__ == '__main__':
    main()
