#!/usr/bin/env python

"""
distutils/setuptools install script.
"""
import os
from setuptools import setup, find_packages

import tencentcloud

ROOT = os.path.dirname(__file__)

setup(
    name='tencent-cloud-python-sdk',
    install_requires=["requests>=2.16.0"],
    version=tencentcloud.__version__,
    description='Python Tencent Cloud SDK',
    long_description=open('README.rst').read(),
    author='hadx',
    url='',
    maintainer_email="",
    scripts=[],
    packages=find_packages(exclude=["tests*"]),
    license="Apache License 2.0",
    platforms='any',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
