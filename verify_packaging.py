# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from __future__ import print_function
import utility
import os
import setup    # called via "verify_package.py clean"" to detect platform for wheel generation.


MSSQLSCRIPTER_DIST_DIRECTORY = os.path.abspath(
    os.path.join(os.path.abspath(__file__), '..', 'dist'))
MSSQLTOOLSSERVICE_DIST_DIRECTORY = os.path.abspath(os.path.join(
    os.path.abspath(__file__), '..', 'mssqltoolsservice', 'dist'))

root_dir = os.path.abspath(os.path.join(os.path.abspath(__file__), '..'))


def build_wheel_for_current_platform():
    """
        Build mssqltoolsservice wheel for current platform.
    """
    # Build mssqltoolsservice wheel for this platform.
    current_platform = os.environ['MSSQLTOOLSSERVICE_PACKAGE_SUFFIX']
    utility.exec_command(
        'python mssqltoolsservice/buildwheels.py {}'.format(current_platform),
        root_dir,
        continue_on_error=False
    )


def verify_local_install():
    """
        Install mssql-scripter package locally that resolves mssqltoolsservice dependency from local build.
    """
    # Local install of mssql-scripter.
    mssqlscripter_sdist_name = os.listdir(MSSQLSCRIPTER_DIST_DIRECTORY)[0]
    # To ensure we have a clean install, we disable the cache as to prevent cache overshadowing actual changes made.
    utility.exec_command(
        'pip install --no-cache-dir --no-index --find-links=./mssqltoolsservice/dist ./dist/{}'.format(mssqlscripter_sdist_name),
        root_dir, continue_on_error=False
    )


if __name__ == '__main__':
    build_wheel_for_current_platform()
    verify_local_install()
