# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import logging
import logging.handlers
import os


def get_config_log_file():

    log_dir = os.path.join(
        os.path.expanduser(
            os.path.join(
                u'~', u'.mssqlscripter')))
    if (not os.path.exists(log_dir)):
        os.makedirs(log_dir)

    return os.path.join(log_dir, u'mssql-scripter.log')

scripter_logger = logging.getLogger('mssqlscripter')
scripter_logger.setLevel(logging.DEBUG)
handler = logging.handlers.RotatingFileHandler(get_config_log_file(), maxBytes=2*1024*1024, backupCount=10)

formatter = logging.Formatter(u'%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
scripter_logger.addHandler(handler)