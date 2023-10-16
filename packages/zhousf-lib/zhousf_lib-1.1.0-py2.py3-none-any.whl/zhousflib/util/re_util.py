# -*- coding: utf-8 -*-
# @Author  : zhousf
# @Function:
import re


def get_digit_char(string: str):
    # 提取数字
    return re.sub(u"([^\u0030-\u0039])", "", string)


def only_contain_letter_char(self, string: str):
    """
    仅包含字母（大小写）
    """
    return len(self.get_letter_char(string)) == len(string)


def get_letter_char(string: str):
    # 提取大小写字母
    return re.sub(u"([^\u0041-\u005a\u0061-\u007a])", "", string)


def get_digit_letter_char(string: str):
    # 提取大小写字母、数字
    return re.sub(u"([^\u0041-\u005a\u0061-\u007a\u0030-\u0039])", "", string)


def only_chinese(string: str):
    """
    string都是中文
    :param string:
    :return: True都是中文 | 否
    """
    match_chinese = re.sub(u"([^\u4e00-\u9fa5])", "", string)
    return len(match_chinese) == len(string)


def normalize_cos_sign(string):
    """
    cos符号标准化：将cos15°转成cos(radians(15))
    cos15° -> cos(radians(15))
    cos5 -> cos(radians(5))
    cosa° -> cos(radians(a))
    cosθ -> cos(radians(θ))
    cos(a) -> cos(radians(a))
    cos(15°) -> cos(radians(15))
    cos(5) -> cos(radians(5))
    :param string:
    :return:
    """
    # ori = string
    items = re.split("[+-/*]", string)
    if len(items) > 0:
        for item in items:
            res = re.findall("[Cc][Oo0][Ss]", item)
            if len(res) > 0:
                value = item.replace(res[0], "").replace("°", "").replace("。", "").replace("(", "").replace(")", "")
                value = "(radians({0}))".format(value)
                string = string.replace(item, "cos" + value)
    # print(ori, "->", side_length)
    return string


def normalize_multiple_sign(string, normalize_char="*"):
    """
    乘号标准化：将x、X、×转成*
    161.9+x2-nXSxd+nxS+2x+2x(a+b) -> 161.9+x2-n*S*d+n*S+2x+2*(a+b)
    :param string:
    :param normalize_char: 标准化的字符
    :return:
    """
    items = re.split("[+-/*]", string)
    if len(items) > 0:
        for item in items:
            res = re.findall("^[^xX×].*[xX×]{1}.*[^xX×]$", item)
            if len(res) > 0:
                item = str(res[0]).replace("x", normalize_char).replace("X", normalize_char).replace("×", normalize_char)
                string = string.replace(res[0], item)
    return string

