# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import io
import threading
import unittest
import mssqlscripter.sqltoolsclient as sql_tools_client


class SqlToolsClientTest(unittest.TestCase):
    """
        SQL Tools Client tests.
    """

    def test_sql_tools_client_initialization(self):
        """
            Verify sql tools client initialization.
        """
        input_stream = io.BytesIO(b'')
        output_stream = io.BytesIO(b'')

        # Start the tools client
        tools_client = sql_tools_client.SqlToolsClient(
            input_stream, output_stream)

        # verify background threads are alive.
        # Until we have a dummy process that blocks on the output_stream, the
        # thread active count when initialized will be 2 (Main and request
        # thread).
        self.assertEqual(threading.active_count(), 2)

        # Create a scripting request with sample parameters.
        parameters = {
            u'FilePath': u'Sample_File_Path',
            u'ConnectionString': u'Sample_connection_string',
            u'DatabaseObjects': None}
        request = tools_client.create_request(
            u'scripting_request', parameters)

        # Assert request is scripting request and hasn't started.
        self.assertIsNotNone(request)
        self.assertFalse(request.completed())

        # Shut down, Request thread should be killed.
        tools_client.shutdown()
        self.assertEqual(threading.active_count(), 1)


if __name__ == u'__main__':
    unittest.main()
