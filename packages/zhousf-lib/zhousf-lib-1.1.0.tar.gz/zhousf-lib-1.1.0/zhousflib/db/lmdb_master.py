# -*- coding: utf-8 -*-
# @Author  : zhousf
# @Function: lmdb (Lightning Memory-Mapped Database) 快如闪电的内存映射数据库
# pip install lmdb
import pickle
import lmdb
from pathlib import Path

"""
实例化数据库
db = LMDB(Path(__file__).parent)
插入数据
db.insert("student", {"a": 99, "b": 95})
删除数据
db.delete("student")
修改数据
db.update("student", {"a": 98, "b": 100})
查询数据
print(db.query("student"))
显示所有数据
db.display()
"""


class LMDB(object):

    def __init__(self, db_dir: Path):
        """
        初始化
        :param db_dir: 文件目录
        """
        self.env = self.initialize(db_dir)

    @staticmethod
    def initialize(db_dir: Path):
        return lmdb.open(path=str(db_dir), map_size=int(1e9))

    def insert(self, key: str, value):
        """
        插入数据
        :param key:
        :param value:
        :return:
        """
        txn = self.env.begin(write=True)
        txn.put(key.encode(), pickle.dumps(value))
        txn.commit()

    def delete(self, key: str):
        """
        删除
        :param key:
        :return:
        """
        txn = self.env.begin(write=True)
        txn.delete(key.encode())
        txn.commit()

    def update(self, key: str, value):
        """
        更新
        :param key:
        :param value:
        :return:
        """
        self.insert(key, value)

    def query(self, key: str):
        """
        查询
        :param key:
        :return:
        """
        txn = self.env.begin()
        res = txn.get(key.encode())
        return None if res is None else pickle.loads(res)

    def display(self):
        """
        显示所有数据
        :return:
        """
        txn = self.env.begin()
        cur = txn.cursor()
        for key, value in cur:
            print(key, pickle.loads(value))

    def clear_all(self):
        """
        删除所有数据
        :return:
        """
        txn = self.env.begin()
        cur = txn.cursor()
        for key, value in cur:
            print(key, pickle.loads(value))
            txn.delete(key.encode())
        txn.commit()

    def close(self):
        self.env.close()


if __name__ == '__main__':
    pass

