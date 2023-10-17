# -*-coding: utf-8 -*-
"""
    @Author : Pan
    @E-mail : 390737991@qq.com
    @Date   : 2022-05-01 16:36:18
    @Url    : https://blog.csdn.net/xiaoyu_wu/article/details/102820384
"""

import time
from typing import List, Callable
from multiprocessing import Pool
from pybaseutils import time_utils


class MultiProcessing(object):
    def __init__(self, max_workers=2):
        """
        :param max_workers:  开启进程数目
        :param maxsize:
        """
        self.executor = Pool(processes=max_workers)

    def task_map2(self, func: Callable, inputs: List):
        """进程任务，返回结果有序(map与submit的性能基本一致)"""
        # 通过executor的 map 获取已经完成的task的值
        result = []
        for r in self.executor.map(func, inputs):
            result.append(r)
        return result

    def task_map(self, func: Callable, inputs: List):
        """进程任务，返回结果有序(map与submit的性能基本一致)"""
        # 通过executor的 map 获取已经完成的task的值
        result = [self.executor.apply_async(func, args=(i,)) for i in inputs]
        result = [r.get() for r in result]
        return result

    def close(self):
        self.executor.close()


def consumer(image_path: str):
    """
    :param image_path:
    :return:
    """
    t = int(image_path.split(".")[0])
    time.sleep(t)
    # with thread_lock:
    print("正在处理数据：{}  ".format(image_path))
    return image_path


if __name__ == "__main__":
    tp = MultiProcessing(max_workers=5)
    # contents = ["1.jpg", "2.jpg", "3.jpg", "4.jpg", "5.jpg"]
    contents = ["1.jpg", "5.jpg", "4.jpg", "3.jpg", "2.jpg"]
    print(contents)
    with time_utils.Performance() as p:
        result1 = tp.task_map(func=consumer, inputs=contents)
    print(result1)
