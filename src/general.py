# -*- coding: utf-8 -*-
import logging
logger = logging.getLogger(__name__)

def bit_seperate_32(n: int):
    """与えられた整数について、各bitの間に0を挟んだ整数に変換する。
    16bitまでの正整数に対応
    """
    n = (n | (n << 8)) & 0x00ff00ff
    n = (n | (n << 4)) & 0x0f0f0f0f
    n = (n | (n << 2)) & 0x33333333
    n = (n | (n << 1)) & 0x55555555
    return n

def get_2d_morton_number(x, y):
    """格子状に切り分けた一領域をモートン番号に変換する。
    x軸方向にx番目、y軸方向にy番目と数える。
    """
    return (bit_seperate_32(x) | (bit_seperate_32(y) << 1))
