# -*- coding:utf-8 -*-
# Author:  zhousf
# Description:
import re

from PIL import ImageFont
from pathlib import Path

# 宋体-汉字
Font_SimSun: Path = Path(__file__).parent.joinpath("SimSun.ttf")

# 符号、数字、字母、数学符号： ①ⓒԑ
Font_SYMBOLA: Path = Path(__file__).parent.joinpath("Symbola.ttf")


def dynamic_font(text: str, font_size: int = 10):
    pattern = re.compile(r'[ⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩ⍺ԑ⍴⍵⍬⍶⍷⍸⍹]')
    if pattern.search(text):
        font = Font_SYMBOLA
    else:
        font = Font_SimSun
    return ImageFont.truetype(font=str(font), size=font_size)
