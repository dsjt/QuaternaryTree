# -*- coding: utf-8 -*-
# 汎用な関数
import math
import itertools
import logging
import matplotlib
import matplotlib.pyplot as plt

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

class AutoSaveFigure(matplotlib.figure.Figure):
    def __init__(self, fn, **kwargs):
        self.fn = fn
        super().__init__(**kwargs)
        pass

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        plt.tight_layout()
        self.savefig(self.fn)
        plt.close(self)
        if exception_type is not None:
            logging.error("Error has occurred.")
            logging.error(exception_type, exception_value, traceback)
        return
