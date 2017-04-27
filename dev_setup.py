# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from __future__ import print_function
from subprocess import check_call, CalledProcessError

import os
import setup
import sys

root_dir = os.path.abspath(os.path.join(os.path.abspath(__file__), '..'))

def exec_command(command):
    try:
        print('Executing: ' + command)
        check_call(command.split(), cwd=root_dir)
        print()
    except CalledProcessError as err:
        print(err, file=sys.stderr)
        sys.exit(1)

print('Running dev setup...')
print('Root directory \'{}\'\n'.format(root_dir))

# install general requirements.
exec_command('pip install -r requirements.txt')

# install mssqltoolsservice if this platform supports it.
mssqltoolsservice_package_name = os.environ['MSSQLTOOLSSERVICE_PACKAGE_NAME']
print('Installing {}...'.format(mssqltoolsservice_package_name))
# mssqltoolsservice package name is retrieved from environment variable set by setup.py.
exec_command('pip install {}'.format(mssqltoolsservice_package_name))

print('Finished dev setup.')
