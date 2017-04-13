# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from __future__ import print_function

import sys
import os
import sqltoolsservicesetup
from subprocess import check_call, CalledProcessError

root_dir = os.path.abspath(os.path.join(os.path.abspath(__file__), '..'))
tools_service_target_dir = os.path.abspath(
    os.path.join(
        root_dir,
        'mssqlscripter',
        'sqltoolsservice'))


def exec_command(command):
    try:
        print('Executing: ' + command)
        check_call(command.split(), cwd=root_dir)
        print()
    except CalledProcessError as err:
        print(err, file=sys.stderr)
        sys.exit(1)


def install_sqltoolsservice():
    download_url = sqltoolsservicesetup.get_download_url()

    if (download_url):
        # This platform supports it, install into the repo
        sqltoolsservicesetup.install(download_url, tools_service_target_dir)
        print('Sql Tools Service was succesfully installed.')
        return
    print('Error: Sql Tools Service is not supported on this platform.')


print('Running dev setup...')
print('Root directory \'{}\'\n'.format(root_dir))

# install general requirements.
exec_command('pip install -r dev_requirements.txt')

# install platform specific sql tools service to repo.
print('Installing native Sql Tools Service...')
install_sqltoolsservice()

print('Finished dev setup.')
