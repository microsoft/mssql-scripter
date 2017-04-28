# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import buildwheels
import os
import sys
from subprocess import check_call, CalledProcessError

MSSQLSCRIPTER_DIST_DIRECTORY = os.path.abspath(os.path.join(os.path.abspath(__file__), '..', 'dist'))
MSSQLTOOLSSERVICE_DIST_DIRECTORY = os.path.abspath(os.path.join(os.path.abspath(__file__), '..', 'mssqltoolsservice', 'dist'))


def register_or_upload_to_pypi(options):
    """
        Registers or uploads against a pypi server.
    """
    supported_actions = ['register', 'upload']

    if len(options) >= 1 and options[0] not in supported_actions:
        print('Please provide a supported action (register or upload).')
        return

    action = options[0]
    repository = ''
    if len(options) == 2:
        # We were provided a explicity repo to target.
        # If no repository was supplied, twine will look for environment variable TWINE_REPOSITORY and/or TWINE_REPOSITORY_URL.
        repository = '-r {}'.format(options[1])
        print('Repository argument was provided, targeting {}'.format(options[1]))

    for wheel_name in os.listdir(MSSQLTOOLSSERVICE_DIST_DIRECTORY):
        # Run twine action for mssqltoolsservice wheels.
        buildwheels.exec_command('twine {} {} {}'.format(action, wheel_name, repository), MSSQLTOOLSSERVICE_DIST_DIRECTORY)

    mssqlscripter_sdist_name = os.listdir(MSSQLSCRIPTER_DIST_DIRECTORY)[0]
    # Run twine action for mssqlscripter.
    buildwheels.exec_command('twine {} {} {}'.format(action, mssqlscripter_sdist_name, repository), MSSQLSCRIPTER_DIST_DIRECTORY)
    
if __name__ == '__main__':
    register_or_upload_to_pypi(sys.argv[1:])
