#!/usr/bin/env python


# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from __future__ import print_function

import os
import platform
import utility
import mssqlscripter.mssqltoolsservice.download as mssqltoolsservice

print('Running dev setup...')
print('Root directory \'{}\'\n'.format(utility.ROOT_DIR))

# install general requirements.
utility.exec_command('pip install -r dev_requirements.txt', utility.ROOT_DIR)
run_time_id = utility.get_current_platform()

if run_time_id:
    mssqltoolsservice.download_mssqltoolsservice(run_time_id)
else:
    print("This platform does not support mssqltoolsservice.")


print('Finished dev setup.')
