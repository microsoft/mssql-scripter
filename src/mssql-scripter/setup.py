# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from setuptools import setup

# Sample set up, will need to update once official files get checked in
setup(
    name='mssql-scripter',
    version='0.1dev',
    package_dir = {'common':'../common'},
    py_modules=['common.json_rpc'],
    packages=['mssql.scripter'],
    license='MIT',
    author='Microsoft Corporation',
    author_email='ssdteng@microsoft.com',
    url='https://github.com/Microsoft/sql-xplat-cli/',
)