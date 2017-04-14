# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import unittest
import mssqlscripter.parser as parser
import os

class TestParser(unittest.TestCase):

    def test_connection_string_builder(self):
        """
            Verify connection string is built correctly based on auth type.
        """
        
        trusted_connection = [u'-S', u'TestServer']
        parameters = parser.parse_arguments(trusted_connection)
        self.assertEqual(parameters.ConnectionString, u'Server=TestServer;Integrated Security=True;')

        trusted_connection = [u'-S', u'TestServer', u'-d', u'mydatabase']
        parameters = parser.parse_arguments(trusted_connection)
        self.assertEqual(parameters.ConnectionString, u'Server=TestServer;Database=mydatabase;Integrated Security=True;')

        trusted_connection = [u'--connection-string', u'Server=TestServer;Database=mydatabase;Integrated Security=True;']
        parameters = parser.parse_arguments(trusted_connection)
        self.assertEqual(parameters.ConnectionString, u'Server=TestServer;Database=mydatabase;Integrated Security=True;')

        standard_connection = [u'-S', u'TestServer', u'-d', u'mydatabase', u'-U', 'my_username', u'-P', 'secret' ]
        parameters = parser.parse_arguments(standard_connection)
        self.assertEqual(parameters.ConnectionString, u'Server=TestServer;Database=mydatabase;User Id=my_username;Password=secret;')

    def test_connection_string_with_environment(self):
        """
            Verify parser picks up connection string and password from environment variable.
        """
        os.environ[parser.MSSQL_SCRIPTER_CONNECTION_STRING] = u'Server=TestServer;Database=mydatabase;User Id=my_username;Password=secret;'
        parameters = parser.parse_arguments(None)
        self.assertEqual(parameters.ConnectionString, 'Server=TestServer;Database=mydatabase;User Id=my_username;Password=secret;')

        standard_connection = [u'-S', u'TestServer', u'-d', u'mydatabase', u'-U', 'my_username']
        #os.environ[parser.MSSQL_SCRIPTER_PASSWORD] = u'secret123ABC'
        parameters = parser.parse_arguments(standard_connection)
        self.assertEqual(parameters.ConnectionString, u'Server=TestServer;Database=mydatabase;User Id=my_username;Password=secret123ABC;')

if __name__ == u'__main__':
    unittest.main()
