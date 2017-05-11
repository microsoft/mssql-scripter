#!/usr/bin/env python


# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from __future__ import print_function

import os
import setup
import utility

root_dir = os.path.abspath(os.path.join(os.path.abspath(__file__), '..'))

print('Running dev setup...')
print('Root directory \'{}\'\n'.format(root_dir))

# install general requirements.
utility.exec_command('pip install -r requirements.txt', root_dir)

# install mssqltoolsservice if this platform supports it.
mssqltoolsservice_package_name = os.environ['MSSQLTOOLSSERVICE_PACKAGE_NAME']
print('Installing {}...'.format(mssqltoolsservice_package_name))
# mssqltoolsservice package name is retrieved from environment variable set by setup.py.
utility.exec_command('pip install {}'.format(mssqltoolsservice_package_name), root_dir)

print('Finished dev setup.')
