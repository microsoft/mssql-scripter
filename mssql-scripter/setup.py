#!/usr/bin/env python

# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
import sys
import sqltoolsservicesetup

from setuptools import setup
from setuptools.command.install import install

VERSION = "0.1.1.dev"


class Install_Native_Dependencies(install):
    """
        Downloads and Installs native sql tools service if platform is supported.
    """

    def run(self):

        sqltoolsservice_url = sqltoolsservicesetup.get_download_url()

        # Only install if sql tools service is supported.
        if sqltoolsservice_url:
            # We only install if sql tools service is supported on this platform.
            # Install sql tools service only if the install was successful; this prevents a dangling sqltoolsservice folder
            # when mssql-scripter was not installed succesfully.
            install.run(self)
            sqltoolsservicesetup.install(sqltoolsservice_url)
            return

        raise EnvironmentError(u'Installation unsuccesful: Sql Tools service is not supported on this platform.')

CLASSIFIERS = [
    u'Development Status :: 2 - Pre-Alpha',
    u'Intended Audience :: Developers',
    u'Intended Audience :: System Administrators',
    u'Programming Language :: Python',
    u'Programming Language :: Python :: 2',
    u'Programming Language :: Python :: 2.7',
    u'Programming Language :: Python :: 3',
    u'Programming Language :: Python :: 3.4',
    u'Programming Language :: Python :: 3.5',
    u'Programming Language :: Python :: 3.6',
    u'License :: OSI Approved :: MIT License',
]

DEPENDENCIES = [
    u'pip',
    u'future',
    u'site'
]

SETUP_DEPENDENCIES = [
    u'requests',
    u'future'
]

if sys.version_info < (3, 4):
    DEPENDENCIES.append(u'enum34')

setup(
    setup_requires=SETUP_DEPENDENCIES,
    install_requires=DEPENDENCIES,
    name=u'mssql-scripter',
    version=VERSION,
    description=u'Microsoft SQL Scripter Command-Line Tool',
    license=u'MIT',
    author=u'Microsoft Corporation',
    author_email=u'sqlxplatclieng@microsoft.com',
    url=u'https://github.com/Microsoft/sql-xplat-cli/',
    zip_safe=True,
    classifiers=CLASSIFIERS,
    include_package_data=True,
    scripts=[
        u'mssql-scripter',
        u'mssql-scripter.bat'
    ],
    packages=[
        u'mssql',
        u'mssql.scripter',
        u'mssql.contracts',
        u'mssql.common'],
    cmdclass={u'install': Install_Native_Dependencies},
)
