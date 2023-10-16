#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import shutil
from setuptools import (
    setup,
    find_packages
)

# 移除构建的build文件夹
CUR_PATH = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(CUR_PATH, 'build')
if os.path.isdir(path):
    print('INFO del dir ', path)
    shutil.rmtree(path)

print("find_packages:", find_packages())

setup(
    name='simmed',
    version='0.2.6',
    description="simmed core sdk",
    author='weizw,lijunhua,zhaoyun',
    author_email='wzw@simmed.cn',
    url='https://simmed.cn',
    install_requires=[
        'flasgger==0.9.5',
        'flask==1.1.2',
        'Flask-Compress==1.10.1',
        'nacos_sdk_python==0.1.6',
        'thriftpy2==0.4.14',
        'py_zipkin==0.20.2',
        'pyctuator==0.17.0',
        'pymongo==3.12.1',
        'PyYAML==5.4.1',
        'requests==2.28.2',
        'Werkzeug==1.0.1',
        'Flask-Cors==3.0.9',
        'redis==3.2.1',
        'pydantic==1.10.5',
        'json-rpc==1.14.0'
    ],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    python_requires='>=3.8, <4',
    keywords='simmed',
    license="MIT",
    packages=find_packages(),
    classifiers=[]
)
