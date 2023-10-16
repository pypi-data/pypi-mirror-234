#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name='dfss',
    version='1.4.13',
    author='zetao.zhang',
    author_email='zetao.zhang@sophgo.com',
    description='download_from_sophon_sftp',
    packages=['dfss'],
    python_requires='>=3.5',
    install_requires=["paramiko","progressbar","ping3"]
)