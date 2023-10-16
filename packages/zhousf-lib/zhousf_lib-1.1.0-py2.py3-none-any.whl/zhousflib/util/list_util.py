# -*- coding:utf-8 -*-
# Author:  zhousf
# Description:  list交集、并集、差集运算
import random
from collections import Counter


def counter(data_list: list, arg=None):
    """
    统计列表中某个元素的个数
    :param data_list: 列表
    :param arg: 某个元素，空时则返回counter
    :return:
    """
    res = Counter(data_list)
    if arg:
        return res.get(arg, 0)
    else:
        return res


def random_choices(data_list: list, choose_k=3) -> list:
    """
    从列表中随机抽取choose_k个数（会有重复值）
    :param data_list:
    :param choose_k:
    :return:
    """
    return random.choices(data_list, k=choose_k)


def none_filter(data: list) -> list:
    """
    去掉list中的None值
    :param data:
    :return:
    """
    if isinstance(data, list):
        res = []
        for item in data:
            if isinstance(item, list):
                res.append(list(filter(None, item)))
            else:
                res = list(filter(None, data))
                break
        return res
    return data


def intersection(a, b):
    """
    交集
    :param a: [1, 2, 3, 4, 5]
    :param b: [2, 3, 9]
    :return: [2, 3]
    """
    if len(a) == 0:
        return b
    if len(b) == 0:
        return a
    return list(set(a).intersection(set(b)))


def union(a, b):
    """
    并集
    :param a: [1, 2, 3, 4, 5]
    :param b: [2, 3, 9]
    :return: [1, 2, 3, 4, 5, 9]
    """
    if len(a) == 0:
        return b
    if len(b) == 0:
        return a
    return list(set(a).union(set(b)))


def difference(a, b):
    """
    差集
    :param a: [1, 2, 3, 4, 5]
    :param b: [2, 3, 9]
    :return: [1, 4, 5]
    """
    if len(a) == 0:
        return b
    if len(b) == 0:
        return a
    return list(set(a).difference(set(b)))


def sort(data: list, index: int = 0, reverse=False):
    """
    排序
    :param data:
    :param index: 排序参考的索引
    :param reverse: 是否倒序
    :return:
    """
    return sorted(data, key=lambda v: v[index], reverse=reverse)
