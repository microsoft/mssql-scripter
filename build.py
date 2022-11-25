#!/usr/bin/env python

# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from __future__ import print_function
import os
import sys
import utility
import mssqlscripter.mssqltoolsservice.external as mssqltoolsservice

AZURE_STORAGE_CONNECTION_STRING = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
BLOB_CONTAINER_NAME = 'simple'
UPLOADED_PACKAGE_LINKS = []


def print_heading(heading, f=None):
    print('{0}\n{1}\n{0}'.format('=' * len(heading), heading), file=f)


def build(platform_names):
    """
        Builds mssql-scripter package.
    """
    print_heading('Cleanup')

    # clean
    utility.clean_up(utility.MSSQLSCRIPTER_DIST_DIRECTORY)

    print_heading('Running setup')

    # install general requirements.
    utility.exec_command('pip install -r dev_requirements.txt', utility.ROOT_DIR)

    # convert windows line endings to unix for mssql-cli bash script
    utility.exec_command('python dos2unix.py mssql-scripter mssql-scripter', utility.ROOT_DIR)

    for platform in platform_names:
        utility.clean_up(utility.MSSQLSCRIPTER_BUILD_DIRECTORY)
        utility.cleaun_up_egg_info_sub_directories(utility.ROOT_DIR)

        mssqltoolsservice.copy_sqltoolsservice(platform)

        print_heading('Building mssql-scripter {} wheel package package'.format(platform))
        utility.exec_command('python --version', utility.ROOT_DIR)
        utility.exec_command(
            'python setup.py check -r -s bdist_wheel --plat-name {}'.format(platform),
            utility.ROOT_DIR,
            continue_on_error=False)
        
        mssqltoolsservice.clean_up_sqltoolsservice()



def validate_package(platform_names):
    """
        Install mssql-scripter wheel package locally.
    """
    root_dir = os.path.abspath(os.path.join(os.path.abspath(__file__), '..'))
    # Local install of mssql-scripter.
    mssqlscripter_wheel_dir = os.listdir(utility.MSSQLSCRIPTER_DIST_DIRECTORY)
    current_platform = utility.get_current_platform()

    mssqlscripter_wheel_name = [pkge for pkge in mssqlscripter_wheel_dir if current_platform in pkge]

    # To ensure we have a clean install, we disable the cache as to prevent cache overshadowing actual changes made.
    utility.exec_command(
       'pip install --no-cache-dir --no-index ./dist/{}'.format(mssqlscripter_wheel_name),
       root_dir, continue_on_error=False)
    

if __name__ == '__main__':
    action = 'build'
    supported_platforms = [
        'win32',
        'win_amd64',
        'macosx_10_11_intel',
        'manylinux1_x86_64']

    targets = {
        'build': build,
        'validate_package': validate_package,
    }

    if len(sys.argv) > 1:
        action = sys.argv[1]
    
    if len(sys.argv) > 2:
        supported_platforms = [sys.argv[2]]
    
    if action in targets:
        targets[action](supported_platforms)
    else:
        print('{} is not a supported action'.format(action))
        print('Supported actions are {}'.format(list(targets.keys())))
