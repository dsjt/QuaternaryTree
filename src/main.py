# -*- coding: utf-8 -*-
import logging
from aabb import Aabb
from lqt import LQT


logging.basicConfig()
logging_levels = {
    "aabb": logging.DEBUG,
    "lqt": logging.DEBUG
}

for mn, level in logging_levels.items():
    logging.getLogger(mn).setLevel(level)

logger = logging.getLogger(__name__)

def main():
    # 一辺100の空間にAabbをよっつ用意。
    a = Aabb([10, 10], [30, 30])
    b = Aabb([20, 20], [40, 40])
    c = Aabb([10, 10], [80, 80])
    d = Aabb([65, 15], [90, 40])

    # 4層、一辺を100として四分木を構成
    lqt = LQT(4, 100)
    lqt.register(a)
    lqt.register(b)
    lqt.register(c)
    lqt.register(d)

    # lqtで接触しているオブジェクトを列挙する
    for x1, x2 in lqt.overlap_pairs():
        print(x1, x2)


if __name__ == '__main__':
    main()
