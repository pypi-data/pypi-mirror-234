# -*- coding: utf-8 -*-
# @Time: 2022/07/12 10:17:09
# @File: setup.py
# @Desc：

import os

from setuptools import setup, find_packages

filepath = os.path.join(os.getcwd(), 'README.md')
setup(
    name="operate_tools",
    version="1.0.6",
    description="Python操作工具合集",
    long_description=open(filepath, encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/Joker-desire/operate-tools",
    author="Joker-desire",
    author_email="2590205729@qq.com",
    requires=['chardet'],
    packages=find_packages(),
    license="MIT Licence",
    platforms="any"
)
