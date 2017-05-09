# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

# Template package that stores native sql tools service binaries during wheel compilation.
# Files will be dynamically created here and cleaned up after each run.

import os
import platform

__version__='1.0.0a1'

def get_executable_path():
    """
        Find mssqltoolsservice executable relative to this package.
    """
    # Debug mode.
    if 'MSSQLTOOLSSERVICE_PATH' in os.environ:
        mssqltoolsservice_base_path = os.environ['MSSQLTOOLSSERVICE_PATH']
    else:
         # Retrieve path to program relative to this package.
        mssqltoolsservice_base_path = os.path.abspath(
            os.path.join(
                os.path.abspath(__file__), 
                '..', 
                'bin')) 

    # Format name based on platform.
    mssqltoolsservice_name = u'Microsoft.SqlTools.ServiceLayer{}'.format(
        u'.exe' if (platform.system() == u'Windows') else u'')
    
    mssqltoolsservice_full_path = os.path.abspath(os.path.join(mssqltoolsservice_base_path, mssqltoolsservice_name))

    if (not os.path.exists(mssqltoolsservice_full_path)):
        error_message = '{} does not exist. Please re-install the mssql-scripter package'.format(mssqltoolsservice_full_path)
        raise EnvironmentError(error_message)

    return mssqltoolsservice_full_path 
