#!/usr/bin/env python
#-*- coding:utf-8 -*-
from setuptools import setup, find_packages

setup(
    name = "qin-cli",
    version = "0.0.1",
    keywords = ("pip"),
    description = "cli tool",
    long_description = "有趣的工具集",
    license = "MIT Licence",
    url = "https://github.com/Alndaly/qin-cli",
    author = "Kinda Hall",
    author_email = "1142704468@qq.com",
    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = []
)