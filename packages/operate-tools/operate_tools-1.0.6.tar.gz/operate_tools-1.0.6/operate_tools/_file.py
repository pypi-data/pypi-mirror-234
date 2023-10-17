# -*- coding: utf-8 -*-
# @Time: 2022/07/20 15:48:19
# @File: _file.py
# @Desc：文件操作


__all__ = ["FileTools"]

import os

from chardet import UniversalDetector


class FileTools:

    @staticmethod
    def encode(file: str) -> str:
        """
        获取文件的编码格式
        :param file: 文件路径
        :return: 编码格式
        """
        with open(file, 'rb') as f:
            detector = UniversalDetector()
            for line in f.readlines():
                detector.feed(line)
                if detector.done:
                    break
            detector.close()
        return detector.result['encoding']

    @staticmethod
    def convert_encode(file: str, encode="utf-8") -> dict:
        """
        编码格式转换
        :param file: 文件路径
        :param encode: 要转换的编码格式. Defaults to "utf-8".
        :return: 转换结果
        """
        original_encode = FileTools.encode(file)
        if original_encode != encode:
            with open(file, 'rb') as f:
                file_content = f.read()
            file_decode = file_content.decode(original_encode, 'ignore')
            file_encode = file_decode.encode(encode)

            with open(file, 'wb') as f:
                f.write(file_encode)
        return {"file": file, "original_encode": original_encode, "now_encode": encode}
