"""
#!/usr/bin/env python
# -*- coding:utf-8 -*-
@File : setup.py
@Author : Zhiyue Chen
@Time : 2023/8/24 14:31
"""
from setuptools import setup, find_packages

setup(
    name='rapBuilder',
    version='0.3.0',
    packages=find_packages(),
    install_requires=[
        'ViennaRNA==2.6.3',
        'tqdm',
    ],
    python_requires='>=3.10',
    platforms='linux_x86_64',
    author='mistyfield',
    author_email='20301050198@fudan.edu',
    description='find optimal RBS and build pRAP system',
    url='https://gitlab.igem.org/2023/software-tools/fudan',
    license='CC BY 4.0',
    license_file='LICENSE',
    project_urls={
        'Wiki': r'https://2023.igem.wiki/fudan/software',
        'Documentation': r'https://mistyfield.github.io/RAP-Docs/'
    }
)
