# -*- coding: utf-8 -*-
import logging
logger = logging.getLogger(__name__)

class QtCell(object):
    """四分木法における空間オブジェクト(Quaternary)
    """
    def __init__(self, depth, morton_order):
        # 自身の空間深さとモートンオーダ
        self.depth = depth
        self.morton_order = morton_order

        # 自身に属するオブジェクト
        self.objects = set()
        pass

    def add(self, obj):
        """空間にオブジェクトを追加する
        """
        self.objects.add(obj)
        return

    def remove(self, obj):
        """空間からオブジェクトを取り除く
        """
        self.objects.remove(obj)
        return

    def __iter__(self):
        return iter(self.objects)

    def __repr__(self):
        return f"<QtCell layer={self.depth}, mn={self.morton_order}>"
