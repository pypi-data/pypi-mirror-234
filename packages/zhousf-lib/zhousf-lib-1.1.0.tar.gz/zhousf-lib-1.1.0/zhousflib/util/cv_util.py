# -*- coding: utf-8 -*-
# @Author  : zhousf
# @Function:
import cv2
import numpy as np
from pathlib import Path


def read(img_path: Path):
    """
    读图片-兼容图片路径包含中文
    :param img_path:
    :return: np.ndarray
    """
    img = cv2.imdecode(np.fromfile(str(img_path), dtype=np.uint8), cv2.IMREAD_COLOR)
    return img


def write(image: np.ndarray, img_write_path: Path):
    """
    写图片-兼容图片路径包含中文
    :param image:
    :param img_write_path:
    :return:
    """
    cv2.imencode(img_write_path.suffix, image[:, :, ::-1])[1].tofile(str(img_write_path))


def max_connectivity_domain(mask_arr: np.array) -> np.array:
    """
    返回掩码中最大的连通域
    :param mask_arr: 二维数组，掩码中0表示背景，1表示目标
    :return:
    """
    # 掩码标识转换
    arr_mask = np.where(mask_arr == 1, 255, 0)
    # 掩码类型转换
    arr_mask = arr_mask.astype(dtype=np.uint8)
    """
    connectivity：可选值为4或8，也就是使用4连通还是8连通
    num：所有连通域的数目
    labels：图像上每一像素的标记，用数字1、2、3…表示（不同的数字表示不同的连通域）
    stats：每一个标记的统计信息，是一个5列的矩阵，每一行对应每个连通区域的外接矩形的x、y、width、height和面积，示例：0 0 720 720 291805
    centroids：连通域的中心点
    """
    nums, labels, stats, centroids = cv2.connectedComponentsWithStats(arr_mask, connectivity=4)
    background = 0
    for row in range(stats.shape[0]):
        if stats[row, :][0] == 0 and stats[row, :][1] == 0:
            background = row
    # 删除背景后的连通域列表
    stats_no_bg = np.delete(stats, background, axis=0)
    # 获取连通域最大的索引
    max_idx = stats_no_bg[:, 4].argmax()
    max_region = np.where(labels == max_idx + 1, 1, 0)
    # 保存
    # cv2.imwrite(r'vis.jpg', max_region * 255)
    return max_region
