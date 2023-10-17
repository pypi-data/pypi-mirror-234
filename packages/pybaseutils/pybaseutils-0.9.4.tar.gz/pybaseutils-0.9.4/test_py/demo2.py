# -*-coding: utf-8 -*-
"""
    @Author : PKing
    @E-mail : 390737991@qq.com
    @Date   : 2022-12-31 11:37:30
    @Brief  : https://blog.csdn.net/qdPython/article/details/121381363
"""
import random
import types
import numpy as np
from pybaseutils import image_utils, file_utils
import cv2


class Base():
    def add(self, a, b):
        info = "Base.add: {}+{}={}".format(a, b, a + b)
        return info


class A1(Base):
    def add1(self, a, b):
        info = "A1.add1: {}+{}={}".format(a, b, a + b)
        return info


class A2(Base):
    def add2(self, a, b):
        info = "A2.add2: {}+{}={}".format(a, b, a + b)
        return info


def fun2(self, a, b):
    info = "fun2: {}+{}={}".format(a, b, a + b)
    return info


if __name__ == '__main__':
    b = Base()
    print("动态获得类方法:", getattr(b, "add")(1, 2))

    b.fun2 = types.MethodType(fun2, b)
    print("动态添加类方法:",b.fun2(3, 4))
