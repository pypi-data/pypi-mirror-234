# -*- coding: utf-8 -*-
import os
from pybaseutils.converter.convert_labelme2voc import Labelme2VOC

if __name__ == "__main__":
    # pip install pybaseutils
    # 将lableme标注的json数据和图片放在同一文件夹
    labelme_data = "/home/PKing/Downloads/test_image"
    out_root = os.path.dirname(labelme_data)
    image_dir = labelme_data
    lm = Labelme2VOC(labelme_data, image_dir)
    lm.build_dataset(out_root, vis=True, crop=False)
