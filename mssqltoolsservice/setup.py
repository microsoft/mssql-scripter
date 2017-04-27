#!/usr/bin/env python

# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from setuptools import setup
import os
import sys

# Version must be in sync with mssqlscripter.
VERSION = "0.1.1.dev0"
# Find the platform we are building against.
# This file should not be called directly.
PLATFORM = os.environ['MSSQLTOOLSSERVICE_PLATFORM']

DEPENDENCIES = [
    'wheel'
]

CLASSIFIERS = [
    'Development Status :: 2 - Pre-Alpha',
    'Intended Audience :: Developers',
    'Intended Audience :: System Administrators',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'License :: OSI Approved :: MIT License',
]


setup(
    install_requires=DEPENDENCIES,
    name='mssqltoolsservice_{0}'.format(PLATFORM),
    version=VERSION,
    description='Microsoft SQL Tools service',
    license='MIT',
    author='Microsoft Corporation',
    author_email='sqlxplatclieng@microsoft.com',
    url='https://github.com/Microsoft/sql-xplat-cli/',
    zip_safe=True,
    classifiers=CLASSIFIERS,
    include_package_data=True,
    packages=[
        'mssqltoolsservice'
    ],
)
