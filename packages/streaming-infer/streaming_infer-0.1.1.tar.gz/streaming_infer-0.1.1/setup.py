#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
Author: liuzixiang
Date: 2023-04-23 19:15:27
LastEditors: liuzixiang
LastEditTime: 2023-07-18 21:12:44
Description: 
"""

from setuptools import setup, find_packages
from pathlib import Path

def read_requirements(path):
    """read requirements"""
    return list(Path(path).read_text().splitlines())[4:]

setup(
    name="streaming_infer",
    version="0.1.1",
    description="streaming_infer",
    author="acg-soe",
    packages=find_packages(),
    url='',
    license='LICENSE.txt',
    python_requires=">=3.9",
    install_requires=read_requirements("requires.txt"),
    )