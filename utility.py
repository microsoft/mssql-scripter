# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from __future__ import print_function
from subprocess import check_call, CalledProcessError
import sys

def exec_command(command, directory):
    """
        Execute command.
    """
    try:
        check_call(command.split(), cwd=directory)
    except CalledProcessError as err:
        print(err, file=sys.stderr)
        sys.exit(1)