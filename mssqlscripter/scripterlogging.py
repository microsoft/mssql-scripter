# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import logging
import logging.handlers
import os


def get_config_log_dir():
    """
        Retrieve logging directory, create it if it doesn't exist.
    """
    if u'XDG_CONFIG_HOME' in os.environ:
        config_home, dir_name = os.environ[u'XDG_CONFIG_HOME'], u'mssqlscripter'
    else:
        config_home, dir_name = u'~', u'.mssqlscripter'

    log_dir = os.path.expanduser(os.path.join(config_home, dir_name))
    if (not os.path.exists(log_dir)):
        os.makedirs(log_dir)
    return log_dir


def get_config_log_file():
    """
        Retrieve log file path.
    """
    return os.path.join(get_config_log_dir(), u'mssql-scripter.log')


def initialize_logger():
    """
        Initializes root logger for scripter with rotating file handler. Should only be called once from main program.
    """
    scripter_logger = logging.getLogger('mssqlscripter')
    scripter_logger.setLevel(logging.DEBUG)
    handler = logging.handlers.RotatingFileHandler(
        get_config_log_file(), maxBytes=2 * 1024 * 1024, backupCount=10)

    formatter = logging.Formatter(
        u'%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    scripter_logger.addHandler(handler)
