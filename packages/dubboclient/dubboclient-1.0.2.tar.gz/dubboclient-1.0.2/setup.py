#!/usr/bin/env python
# -*- coding:utf-8 -*-
from setuptools import setup, find_packages

setup(
    name="dubboclient",
    version="1.0.2",
    keywords=["pip", "dubboclient", "DubboClient", "dubbo"],
    description="A client tool for testing the Dubbo API",
    long_description="A client tool based on the telnetlib library for testing the Dubbo API",
    license="MIT Licence",

    url="https://github.com/likgjava/dubboclient",
    author="outman",
    author_email="likg.java@163.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=[]
)
