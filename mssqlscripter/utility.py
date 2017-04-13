# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import os
import platform
import site


# Check repo if in dev mode.
TOOLS_SERVICE_DIR = os.path.abspath(
    os.path.join(
        os.path.abspath(__file__),
        u'..',
        u'sqltoolsservice'))

if (not os.path.exists(TOOLS_SERVICE_DIR)):
    # Production mode.
    for path in site.getsitepackages():
        if (path.endswith(u'site-packages')):
            TOOLS_SERVICE_DIR = os.path.join(
                path, u'mssqlscripter', u'sqltoolsservice')
            break


def get_sql_tools_service_path():
    """
        Retrieves Sql tools service program path.
    """
    sql_tools_service_file_name = u'Microsoft.SqlTools.ServiceLayer{}'.format(
        u'.exe' if (platform.system() == u'Windows') else u'')

    sql_tools_service_path = os.path.join(
        TOOLS_SERVICE_DIR.lower(), sql_tools_service_file_name)

    if (not os.path.exists(sql_tools_service_path.strip())):
        error_message = u'{} does not exist. mssql-scripter may be corrupted, please reinstall.'.format(
            sql_tools_service_path)
        raise EnvironmentError(error_message)

    return sql_tools_service_path