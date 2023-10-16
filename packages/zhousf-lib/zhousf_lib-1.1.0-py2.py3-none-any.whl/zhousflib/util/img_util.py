# -*- coding:utf-8 -*-
# Author:  zhousf
# Description:
import imghdr
import base64
import hashlib
from pathlib import Path


def get_file_base64(file_path: Path, contain_file_name=False, split_char=","):
    """
    图片转base64
    :param file_path: 图片路径
    :param contain_file_name: 是否包含文件名称
    :param split_char: 分隔符
    :return: 'a.jpg,iVBORw0KGgoAAAANSUhEUgAABNcAAANtCAYAAACzHZ25AAA.....'
    """
    with file_path.open('rb') as infile:
        s = infile.read()
    base64_str = base64.b64encode(s).decode("utf-8")
    if contain_file_name:
        base64_str = file_path.name + split_char + base64_str
    return base64_str


def md5(file_path: Path):
    with file_path.open('rb') as f:
        return hashlib.md5(f.read()).hexdigest()


def rename_image_with_md5(src_dir: Path, dst_dir: Path):
    if not dst_dir.exists():
        dst_dir.mkdir()
    count = 0
    repeat = 0
    for file in src_dir.rglob("*.*"):
        if not imghdr.what(str(file)):
            continue
        print(file.name)
        count += 1
        new_name = md5(file)
        new_name += file.suffix
        print(new_name)
        if dst_dir.joinpath(new_name).exists():
            repeat += 1
            continue
        if not dst_dir.joinpath(file.parent.name).exists():
            dst_dir.joinpath(file.parent.name).mkdir(parents=True)
        if not dst_dir.joinpath(file.parent.name).joinpath(new_name).exists():
            file.rename(dst_dir.joinpath(file.parent.name).joinpath(new_name))
    print("count=", count)
    print("repeat=", repeat)


if __name__ == "__main__":
    pass
