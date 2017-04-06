# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import sys
import os

import mssql.scripter.main

try:
    # TODO: Start telemetry here
    args = sys.argv[1:]
    exit_code = mssql.scripter.main.main(args)

    # TODO: Log telemetry based on exit code
    sys.exit(exit_code)
except EnvironmentError as error:
    sys.stdout.write(str(e))
    sys.exit(1)
except KeyboardInterrupt:
    sys.exit(2)
