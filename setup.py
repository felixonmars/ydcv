#!/usr/bin/env python
import sys
from setuptools import setup

setup_requires = ['setuptools_scm']
if sys.argv[-1] in ('sdist', 'bdist_wheel'):
    setup_requires.append('setuptools-markdown')


setup(
    name="ydcv",
    version="0.0.1",
    description="YouDao Console Version, a simple wrapper for Youdao API",
    long_description_markdown_filename='README.md',
    author="Felix Yan",
    author_email="felixonmars@archlinux.org",
    url="https://github.com/felixonmars/ydcv",
    license="GPL",
    package_dir={'': 'src'},
    py_modules=['ydcv'],
    entry_points={
        'console_scripts': ['ydcv=ydcv:main'],
    },
    setup_requires=setup_requires,
    use_scm_version=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: SunOS/Solaris",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Utilities",
    ]
)
