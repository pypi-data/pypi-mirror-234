'''
Date         : 2022-10-25 15:44:41
Author       : BDFD,bdfd2005@gmail.com
Github       : https://github.com/bdfd
LastEditTime : 2023-10-11 16:39:48
LastEditors  : BDFD
Description  : 
FilePath     : \setup.py
Copyright (c) 2022 by BDFD, All Rights Reserved. 
'''
from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

VERSION = '2.1.2'
DESCRIPTION = 'Preprocessing dataset'
PACKAGE_NAME = 'execdata'

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    author="BDFD",
    author_email="bdfd2005@gmail.com",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bdfd",
    project_urls={
        "Bug Tracker": "https://github.com/bdfd",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    python_requires=">=3.6",
)
