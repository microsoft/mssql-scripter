#!/usr/bin/env python

# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import io
import os
import platform as _platform
import sys

from setuptools import setup

MSSQLSCRIPTER_VERSION = '1.0.0a21'


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

DEPENDENCIES = [
    'future>=0.16.0',
    'wheel>=0.29.0'
]

if sys.version_info < (3, 4):
    DEPENDENCIES.append('enum34>=1.1.6')

setup(
    install_requires=DEPENDENCIES,
    name='mssql-scripter',
    version=MSSQLSCRIPTER_VERSION,
    description='Microsoft SQL Scripter Command-Line Tool',
    license='MIT',
    author='Microsoft Corporation',
    author_email='sqlcli@microsoft.com',
    url='https://github.com/Microsoft/mssql-scripter/',
    zip_safe=True,
    long_description=open('README.rst').read(),
    classifiers=CLASSIFIERS,
    include_package_data=True,
    scripts=[
        'mssql-scripter',
        'mssql-scripter.bat'
    ],
    packages=[
        'mssqlscripter',
        'mssqlscripter.mssqltoolsservice',
        'mssqlscripter.jsonrpc',
        'mssqlscripter.jsonrpc.contracts'],
)
