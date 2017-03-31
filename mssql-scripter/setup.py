#!/usr/bin/env python

# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import sys
import os
import platform as _platform

from setuptools import setup
from setuptools.command.install import install

# TODO: Decide on versioning
VERSION = "0.1.1.dev"

# TODO Find linux distro based on https://www.freedesktop.org/software/systemd/man/os-release.html
class Install_Native_Dependencies(install):
    #   win7-x64
    #   win7-x86
    #   osx.10.11-x64
    #   ubuntu.14.04-x64
    #   ubuntu.16.04-x64
    #   centos.7-x64
    #   rhel.7.2-x64
    #   debian.8-x64
    #   fedora.23-x64
    #   opensuse.13.2-x64

    def run(self):

        current_platform = _platform.system()
        architecture = _platform.architecture()
        version = _platform.version()

        print('------------DEBUG-------------\n')
        print('platform: {0}'.format(current_platform))
        print('architecture: {0}'.format(architecture))
        print('version: {0}'.format(version))

        if (current_platform == 'windows'):
            pass
        elif (current_platform == 'Darwin'):
            pass
        elif (current_platform == 'Linux'):
            pass

        install.run(self)

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
    'future'
]

if sys.version_info < (3, 4):
    DEPENDENCIES.append('enum34')

setup(
    cmdclass={'install' : Install_Native_Dependencies},
    name='mssql-scripter',
    version=VERSION,
    description='Microsoft SQL Scripter Command-Line Tool',
    license='MIT',
    author='Microsoft Corporation',
    author_email='sqlxplatclieng@microsoft.com',
    url='https://github.com/Microsoft/sql-xplat-cli/',
    zip_safe=True,
    classifiers=CLASSIFIERS,
    #include_package_data=True,
    scripts=[
        'mssql-scripter',
        'mssql-scripter.bat'
    ],
    packages=[
        'mssql',
        'mssql.scripter',
        'mssql.contracts',
        'mssql.common'],
    install_requires=DEPENDENCIES
)

