#!/usr/bin/env python

# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
import sys
import nativesetup

from setuptools import setup
from setuptools.command.install import install

# TODO: Decide on versioning
VERSION = "0.1.1.dev"


class Install_Native_Dependencies(install):
    """
        Downloads and Installs native sql tools service if platform is supported.
    """

    def run(self):

        runtime_id = nativesetup.get_native_runtime_id()
        native_dependecy_link = nativesetup.get_native_dependency_path(
            runtime_id)

        # Only install if sql tools service is supported.
        if (native_dependecy_link):
            install.run(self)
            nativesetup.install_native_sql_tools_service(native_dependecy_link)


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
    'pip',
    'future',
    'site'
]

SETUP_DEPENDENCIES = [
    'requests',
    'future'
]

if sys.version_info < (3, 4):
    DEPENDENCIES.append('enum34')

setup(
    setup_requires=SETUP_DEPENDENCIES,
    install_requires=DEPENDENCIES,
    name='mssql-scripter',
    version=VERSION,
    description='Microsoft SQL Scripter Command-Line Tool',
    license='MIT',
    author='Microsoft Corporation',
    author_email='sqlxplatclieng@microsoft.com',
    url='https://github.com/Microsoft/sql-xplat-cli/',
    zip_safe=True,
    classifiers=CLASSIFIERS,
    include_package_data=True,
    scripts=[
        'mssql-scripter',
        'mssql-scripter.bat'
    ],
    packages=[
        'mssql',
        'mssql.scripter',
        'mssql.contracts',
        'mssql.common'],
    cmdclass={'install': Install_Native_Dependencies},
)
