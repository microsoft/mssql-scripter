# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

# Template package that stores native sql tools service binaries during wheel compilation.
# Files will be dynamically created here and cleaned up after each run.

import os
import platform

def get_mssqltoolsservice_program():
    """
        Find mssqltoolsservice executable relative to this package.
    """
    # Format name based on platform.
    mssqltoolsservice_name = u'Microsoft.SqlTools.ServiceLayer{}'.format(
        u'.exe' if (platform.system() == u'Windows') else u'')
    
    # Retrieve path to program relative to this package.
    mssqltoolsservice_path = os.path.abspath(
            os.path.join(
                os.path.abspath(__file__), 
                '..', 
                'bin', 
                mssqltoolsservice_name))

    if (not os.path.exists(mssqltoolsservice_path)):
        error_message = '{} does not exist. Please re-install the mssql-scripter package'.format(mssqltoolsservice_path)
        raise EnvironmentError(error_message)

    return mssqltoolsservice_path 
