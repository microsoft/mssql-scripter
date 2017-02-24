# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------


from common.json_rpc import Json_Rpc_Reader
from common.json_rpc import Json_Rpc_Writer
from common.json_rpc import Read_State

from io import BytesIO
import unittest

class Mssql_Scripter_Test(unittest.TestCase):
    """
        Sample Scripter test
    """
    def test_create_rpc_reader(self):
        test_stream = BytesIO(b'Content-Length: 15\r\n\r\n{"key":"value"}')
        json_rpc_reader = Json_Rpc_Reader(test_stream)
        response = json_rpc_reader.read_response()
        baseline = {"key":"value"}
        self.assertEqual(response, baseline)
        
if __name__ == '__main__':
    unittest.main()
