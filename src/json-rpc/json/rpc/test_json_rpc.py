# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from json_rpc import JSON_RPC_Reader
from json_rpc import JSON_RPC_Writer

from io import BytesIO
import unittest

class JSON_RPC_Test(unittest.TestCase):

    def test_basic_response(self):
        test_stream = BytesIO(b'Content-Length: 15\r\n\r\n{"key":"value"}')
        json_rpc_reader = JSON_RPC_Reader(test_stream)
        response = json_rpc_reader.read_response()
        baseline = {"key":"value"}
        self.assertEqual(response, baseline)
        
    def test_basic_request(self):
        test_stream = BytesIO()
        json_rpc_writer = JSON_RPC_Writer(test_stream)
        json_rpc_writer.send_request(method="testMethod/DoThis", params={"Key":"Value"}, id=1)

        # Use JSON RPC reader to read request
        test_stream.seek(0)
        json_rpc_reader = JSON_RPC_Reader(test_stream)
        response = json_rpc_reader.read_response()
        baseline = {"jsonrpc": "2.0", "params": {"Key": "Value"}, "method": "testMethod/DoThis", "id": 1}
        self.assertEqual(response, baseline)

    def test_nested_request(self):
        test_stream = BytesIO()
        json_rpc_writer = JSON_RPC_Writer(test_stream)
        json_rpc_writer.send_request(method="testMethod/DoThis", params={"Key":"Value", "key2": {"key3":"value3", "key4":"value4"}}, id=1)

        # Use JSON RPC reader to read request
        test_stream.seek(0)
        json_rpc_reader = JSON_RPC_Reader(test_stream)
        response = json_rpc_reader.read_response()
        baseline = {"jsonrpc": "2.0", "params": {"Key":"Value", "key2": {"key3":"value3", "key4":"value4"}}, "method": "testMethod/DoThis", "id": 1}
        self.assertEqual(response, baseline)

    def test_response_multiple_headers(self):
        test_stream = BytesIO(b'Content-Length: 15\r\nHeader2: content2\r\nHeader3: content3\r\n\r\n{"key":"value"}')
        json_rpc_reader = JSON_RPC_Reader(test_stream)
        response = json_rpc_reader.read_response()
        baseline = {"key":"value"}
        self.assertEqual(response, baseline)

    def test_incorrect_header_format(self):       
        # Verify end of stream thrown with invalid header
        with self.assertRaises(EOFError):
            test_stream = BytesIO(b'Content-Length: 15\r\n{"key":"value"}')
            json_rpc_reader = JSON_RPC_Reader(test_stream)
            response = json_rpc_reader.read_response()

    def test_invalid_json_response(self):
        # Verify error thrown with invalid JSON
        with self.assertRaises(ValueError):
            test_stream = BytesIO(b'Content-Length: 14\r\n\r\n{"key":"value"')
            json_rpc_reader = JSON_RPC_Reader(test_stream)
            response = json_rpc_reader.read_response()

    def test_stream_closes_during_read_and_write(self):
        test_stream = BytesIO()
        json_rpc_writer = JSON_RPC_Writer(test_stream)
        json_rpc_writer.send_request(method="testMethod/DoThis", params={"Key":"Value"}, id=1)

        # reset the stream
        test_stream.seek(0)
        json_rpc_reader = JSON_RPC_Reader(test_stream)
        # close the stream
        test_stream.close()
        with self.assertRaises(ValueError):
            response = json_rpc_reader.read_response()

    def test_trigger_buffer_resize(self):
        test_stream = BytesIO(b'Content-Length: 15\r\n\r\n{"key":"value"}')
        json_rpc_reader = JSON_RPC_Reader(test_stream)
        # set the message buffer to a small size triggering a resize
        json_rpc_reader.buffer = bytearray(2)
        # Initial size set to 2 bytes
        self.assertEqual(len(json_rpc_reader.buffer), 2)
        response = json_rpc_reader.read_response()
        baseline = {"key":"value"}
        self.assertEqual(response, baseline)
        # Verify message buffer was reset to it's default max size
        self.assertEqual(len(json_rpc_reader.buffer), 8192)
        
    def test_max_buffer_resize(self):
        test_stream = BytesIO(b'Content-Length: 15\r\n\r\n{"key":"value"}')
        json_rpc_reader = JSON_RPC_Reader(test_stream)
        # Double buffer size to max to verify resize takes leftover size which should be larger than default max buffer size
        json_rpc_reader.buffer = bytearray(16384)
        # Verify initial buffer size was set
        self.assertEqual(len(json_rpc_reader.buffer), 16384)
        response = json_rpc_reader.read_response()
        baseline = {"key":"value"}
        self.assertEqual(response, baseline)
        # Verify buffer size decreased by bytes_read
        self.assertEqual(len(json_rpc_reader.buffer), 16347)

if __name__ == '__main__':
    unittest.main()
    