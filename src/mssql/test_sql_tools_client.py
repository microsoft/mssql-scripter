# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import unittest

from mssql.scripter.sql_tools_client import Sql_Tools_Client

class Sql_Tools_Client_Test(unittest.TestCase):
    """
        Test cases for verifying Sql Tools Client
    """
    def test_sql_tools_client_initialization(self):
        tools_client = Sql_Tools_Client(None, None)