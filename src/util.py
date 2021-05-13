# -*- coding: utf-8 -*-
# 汎用な関数
import math
import itertools
import logging

logger = logging.getLogger(__name__)

def flatten(list_of_lists):
    "Flatten one level of nesting"
    return itertools.chain.from_iterable(list_of_lists)

def bit_n_most(v: int):
    """
    整数の最上位bitを得る。
    """
    if v == 0:
        return 0
    else:
        return len(bin(v))-2
