# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from __future__ import print_function

import sys
import os
from subprocess import check_call, CalledProcessError

root_dir = os.path.abspath(os.path.join(os.path.abspath(__file__), '..'))

def exec_command(command):
    try:
        print('Executing: ' + command)
        check_call(command.split(), cwd=root_dir)
        print()
    except CalledProcessError as err:
        print(err, file=sys.stderr)
        sys.exit(1)


def install_mssqltoolsservice():
    import dev_mssqltoolsservicesetup
    
    mssqltoolsservice_package_name = dev_sqltoolsservicesetup.get_mssqltoolsservice_if_supported()
    if mssqltoolsservice_package_name:
        exec_command('pip install {}'.format(mssqltoolsservice_package_name))
        print('{} was succesfully installed.'.format(mssqltoolsservice_package_name))
        return

    print('Error: mssqltoolsservice is not supported on this platform.')


print('Running dev setup...')
print('Root directory \'{}\'\n'.format(root_dir))

# install general requirements.
exec_command('pip install -r requirements.txt')

# install mssqltoolsservice if this platform supports it.
print('Installing mssqltoolsservice...')
install_mssqltoolsservice()

print('Finished dev setup.')
