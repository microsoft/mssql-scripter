#!/usr/bin/env python

# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from setuptools import setup
import sys
#TODO: Decide on versioning
VERSION = "0.1.1dev"

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

DEPENDENCIES = [
    'pip'
]

if sys.version_info < (3, 4):
    DEPENDENCIES.append('enum34')

setup(
    name='mssql-scripter',
    version=VERSION,
    description='Microsoft SQL Scripter Command-Line Tool',
    license='MIT',
    author='Microsoft Corporation',
    author_email='sqlxplatclieng@microsoft.com',
    url='https://github.com/Microsoft/sql-xplat-cli/',
    zip_safe=False,
    classifiers=CLASSIFIERS,
    include_package_data=True,
    scripts =[
        'mssql-scripter',
        'mssql-scripter.bat'
    ],
    packages=[
        'mssql',
        'mssql.scripter', 
        'mssql.requests', 
        'mssql-common'],
    install_requires=DEPENDENCIES
)
