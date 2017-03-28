# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import unittest
import threading

from mssql.client import Sql_Tools_Client
from mssql.requests.scripting import *
from io import BytesIO, BufferedReader

class Sql_Tools_Client_Test(unittest.TestCase):
    """
        Test cases for verifying Sql Tools Client.
    """
    def test_sql_tools_client_initialization(self):
        input_stream = BytesIO(b'')
        output_stream = BytesIO(b'')
        
        # Start the tools client
        tools_client = Sql_Tools_Client(input_stream, output_stream)

        # verify background threads are alive
        # Until we have a dummy process that blocks on the output_stream, the thread active count when initialized will be 2 (Main and request thread)
        self.assertEqual(threading.active_count(), 2)

        # Create a scripting request with sample parameters
        parameters = {'FilePath': 'Sample_File_Path', 'ConnectionString': 'Sample_connection_string', 'DatabaseObjects' : None}
        request = tools_client.create_request_factory('scripting_request', parameters)

        # Assert request is scripting request and hasn't started
        self.assertTrue(isinstance(request, Scripting_Request))
        self.assertFalse(request.completed())

        # Shut down, Request thread should be killed
        tools_client.shutdown()
        self.assertEqual(threading.active_count(), 1)

if __name__ == '__main__':
    unittest.main()
