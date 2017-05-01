#!/usr/bin/env python

# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from setuptools import setup
import os
import sys

# This version number is in place in two places and must be in sync with mssqlscripter's version in setup.py.
MSSQTOOLSSERVICE_VERSION = "0.1.1a12"
# Find the platform we are building against.
# This file should not be called directly.
PLATFORM = os.environ['MSSQLTOOLSSERVICE_PLATFORM']

CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
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
    name='mssqltoolsservice_{}'.format(PLATFORM),
    version=MSSQTOOLSSERVICE_VERSION,
    description='Microsoft SQL Tools Service',
    license='MIT',
    author='Microsoft Corporation',
    author_email='sqlxplatclieng@microsoft.com',
    url='https://github.com/Microsoft/sqltoolsservice',
    zip_safe=True,
    classifiers=CLASSIFIERS,
    include_package_data=True,
    packages=[
        'mssqltoolsservice'
    ],
)
