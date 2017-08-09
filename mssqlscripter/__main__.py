# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import sys

import mssqlscripter.main

try:
    args = sys.argv[1:]
    exit_code = mssqlscripter.main.main(args)
    sys.exit(exit_code)
except EnvironmentError as error:
    sys.stderr.write(str(error))
    sys.exit(1)
except KeyboardInterrupt as error:
    sys.exit(2)
except Exception as error:
    sys.stderr.write(str(error))
    sys.exit(3)
