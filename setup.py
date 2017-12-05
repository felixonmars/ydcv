#!/usr/bin/env python
from setuptools import setup

with open('README.md') as f:
    long_description = f.read().strip()


setup(
    name="ydcv",
    version="0.0.1",
    description="YouDao Console Version, a simple wrapper for Youdao API",
    long_description=long_description,
    # classifiers=[],
    # keywords="",
    author="Felix Yan",
    author_email="felixonmars@archlinux.org",
    url="https://github.com/felixonmars/ydcv",
    # license="",
    package_dir={'': 'src'},
    py_modules=['ydcv'],
    entry_points={
        'console_scripts': ['ydcv=ydcv:main'],
    },
)
