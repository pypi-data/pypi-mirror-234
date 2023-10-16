# -*- coding:utf-8 -*-
# Author:      zhousf
# Description:  批量异步下载工具类
"""
pip install grequests
"""
import os
import time
import grequests
from requests import Response


class DownloadBatch(object):

    def __init__(self, save_dir, concurrent=True):
        """
        批量下载文件工具类
        :param save_dir: 保存文件目录
        :param concurrent: True并行  False串行
        """
        self.save_dir = save_dir
        self.req_list = []
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        self.consume_time = 0
        self.file_names = []
        self.task_num = 0
        self.concurrent = concurrent

    @staticmethod
    def exception_handler(request, exception):
        r = Response()
        r.status_code = 408
        r.reason = "download failed"
        return r

    def add(self, name, url, timeout=20.0):
        """

        :param name:
        :param url:
        :param timeout:
        :return:
        """
        if url is None or name is None:
            return False
        if name in self.file_names:
            return False
        self.file_names.append(name)
        self.req_list.append(grequests.get(url, timeout=timeout))
        return True

    def add_all(self, files):
        """

        :param files: [{"name": "1.jpg", "url": ""}]
        :return:
        """
        for file in files:
            name = file.get("name")
            url = file.get("url")
            if url is None or name is None:
                continue
            timeout = file.get("timeout", default=20.0)
            self.req_list.append(grequests.get(url, timeout=timeout))
            self.file_names.append(name)

    def run(self):
        """

        :return:
        """
        result = {}
        start = time.time()
        self.task_num = len(self.req_list)
        if self.task_num == 0:
            return result
        size = self.task_num if self.concurrent else 1
        responses = grequests.map(requests=self.req_list, size=size, exception_handler=self.exception_handler)
        for i in range(0, len(responses)):
            response = responses[i]
            try:
                save_file = "{0}/{1}".format(self.save_dir, self.file_names[i])
                target_type = self.file_names[i].split(".")[-1]
                if 'Content-Type' in response.headers:
                    content_type = response.headers['Content-Type']
                    if target_type in ["jpg", "JPG", "JPEG", "jpeg", "png", "PNG", "gif", "GIF"]:
                        target_type = "image"
                    if content_type.find(target_type) < 0:
                        result[self.file_names[i]] = (False,
                                                      "The file type is {0}, but {1} is expected. {2}".format(
                                                          content_type,
                                                          target_type,
                                                          response.text),
                                                      self.req_list[i].url)
                        continue
                if response.status_code != 200:
                    result[self.file_names[i]] = (
                        False, "{0}({1})".format(response.text, response.status_code), self.req_list[i].url)
                    continue
                # 当信息流小于100字节，则不是文件
                if len(response.text) <= 100:
                    result[self.file_names[i]] = (
                        False, "{0}({1})".format(response.text, response.status_code), self.req_list[i].url)
                    continue
                with open(save_file, "wb") as f:
                    f.write(response.content)
                    result[self.file_names[i]] = (True, save_file, self.req_list[i].url)
            except Exception as ex:
                result[self.file_names[i]] = (
                    False, "{0}({1})".format(response.text, response.status_code), self.req_list[i].url)
                continue
        end = time.time()
        self.consume_time = end - start
        return result


if __name__ == "__main__":
    url = ""
    downloader = DownloadBatch(save_dir="/home/ubuntu/Downloads")
    downloader.add(name="1.jpg", url=url, timeout=6)
    downloader.add(name="2.jpg", url=url, timeout=0.005)
    results = downloader.run()
    for result in results:
        success, save_file, url = results.get(result)
        print(result, success, save_file, url)
    print("cost time: {0}s | 共{1}项".format(downloader.consume_time, downloader.task_num))
