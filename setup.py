#!/usr/bin/env python

from setuptools import setup

setup(
    name='osx-tags',
    version='0.1',
    packages=['osx_tags'],
    description='Module to manipulate Finder tags on OS X',
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    install_requires=[
        'biplist',
        'xattr',
    ],
    license='MIT',
    zip_safe=True
)