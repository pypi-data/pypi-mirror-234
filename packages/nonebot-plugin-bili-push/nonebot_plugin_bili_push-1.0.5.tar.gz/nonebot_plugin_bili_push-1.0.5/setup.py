#!/usr/bin/env python
# -*- coding:utf-8 -*-
from setuptools import setup, find_packages

# python.exe setup.py sdist bdist_wheel
# twine upload dist/*
# del ./build
# del ./dist
# del ./nonebot_plugin_bili_push.egg-info


def get_install_requires():
    reqs = [
        'pillow>=9.5.0',
        'httpx>=0.24.1',
        'requests>=2.31.0',
        'toml>=0.10.2',
        'nonebot2>=2.0.0',
        'nonebot_adapter_onebot>=2.2.3',
        'nonebot_plugin_apscheduler>=0.2.0'
    ]
    return reqs


setup(name='nonebot_plugin_bili_push',
      version='1.0.5',
      description='nonebot plugin bili push',
      author='SuperGuGuGu',
      author_email='13680478000@163.com',
      url='https://github.com/SuperGuGuGu/nonebot_plugin_bili_push',
      packages=find_packages(),
      python_requires=">=3.8",
      install_requires=get_install_requires(),
      # package_data={'': ['*.csv', '*.txt', '.toml']},
      include_package_data=True
      )
