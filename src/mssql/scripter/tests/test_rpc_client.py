# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from mssql.scripter.rpc_client import Rpc_Client
from io import BytesIO

import unittest
import threading

class Rpc_Client_Tests(unittest.TestCase):

    def test_request_enqueued(self):
        input_stream = BytesIO()
        output_stream = BytesIO(b'sample output')

        test_client = Rpc_Client(input_stream, output_stream)
        test_client.submit_request('scriptingService/ScriptDatabase', {'ScriptDatabaseOptions':'True'})
        
        request = test_client.request_queue.get()
        self.assertEqual(request['method'], 'scriptingService/ScriptDatabase')
        self.assertEqual(request['params'], {'ScriptDatabaseOptions' :'True'})
    
    def test_response_dequeued(self):
        input_stream = BytesIO()
        output_stream = BytesIO(b'Content-Length: 15\r\n\r\n{"key":"value"}')

        test_client = Rpc_Client(input_stream, output_stream)
        test_client.start()
        self.shutdown_background_threads(test_client)

        response = test_client.response_queue.get()
        baseline = {"key":"value"}
        self.assertEqual(response, baseline)
        
        self.assertFalse(test_client.request_thread.isAlive())
        self.assertFalse(test_client.response_thread.isAlive())
        self.assertEqual(threading.active_count(), 1)

    def test_submit_simple_request(self):
        input_stream = BytesIO()
        output_stream = BytesIO(b'Content-Length: 15\r\n\r\n{"key":"value"}')

        test_client = Rpc_Client(input_stream, output_stream)
        test_client.start()

        # Verify threads are alive and running
        self.assertTrue(test_client.request_thread.isAlive())
        self.assertTrue(test_client.response_thread.isAlive())
        self.assertEqual(threading.active_count(), 3)

        test_client.submit_request('scriptingService/ScriptDatabase', {'ScriptDatabaseOptions':'True'})

        self.shutdown_background_threads(test_client)

        # check stream contents
        input_stream.seek(0)
        expected = 'Content-Length: 120\r\n\r\n{"params": {"ScriptDatabaseOptions": "True"}, "jsonrpc": "2.0", "method": "scriptingService/ScriptDatabase", "id": null}'
        
        self.assertEqual(input_stream.getvalue(), expected)
        self.assertFalse(test_client.request_thread.isAlive())
        self.assertFalse(test_client.response_thread.isAlive())
        self.assertEqual(threading.active_count(), 1)

    def test_normal_shutdown(self):
        input_stream = BytesIO()
        output_stream = BytesIO(b'Content-Length: 15\r\n\r\n{"key":"value"}')

        test_client = Rpc_Client(input_stream, output_stream)
        test_client.start()

        # Verify threads are alive and running
        self.assertTrue(test_client.request_thread.isAlive())
        self.assertTrue(test_client.response_thread.isAlive())
        self.assertEqual(threading.active_count(), 3)

        test_client.shutdown()

        self.assertFalse(test_client.request_thread.isAlive())
        self.assertFalse(test_client.response_thread.isAlive())
        self.assertEqual(threading.active_count(), 1)

    #def test_send_multiple_request(self):
    #    input_stream = BytesIO()
    #    output_stream = BytesIO(b'Content-Length: 15\r\n\r\n{"key":"value"}')
    #
    #    test_client = Rpc_Client(input_stream, output_stream)
    #    test_client.start()
    #
    #    # Verify threads are alive and running
    #    self.assertTrue(test_client.request_thread.isAlive())
    #    self.assertTrue(test_client.response_thread.isAlive())
    #    self.assertEqual(threading.active_count(), 3)
    #
    #    test_client.submit_request('scriptingService/ScriptDatabase', {'ScriptDatabaseOptions' : 'True'})
    #    test_client.submit_request('scriptingService/ScriptDatabase', {'ScriptCollations' : 'True'})
    #    test_client.submit_request('scriptingService/ScriptDatabase', {'ScriptDefaults' : 'True'})
    #
    #   TODO: Need to let the thread run a bit to process the requests before reading from the stream
    #  
    #    self.shutdown_background_threads(test_client)
    #    self.assertFalse(test_client.request_thread.isAlive())
    #    self.assertFalse(test_client.response_thread.isAlive())
    #    self.assertEqual(threading.active_count(), 1)

    def test_send_invalid_request(self):
        """
            Verifies that a request with a null method or parameter is not enqueued
        """
        input_stream = BytesIO()
        output_stream = BytesIO(b'sample output')

        test_client = Rpc_Client(input_stream, output_stream)
        self.assertFalse(test_client.submit_request(None, None))

    def test_receive_invalid_response(self):
        pass

    def test_stream_has_no_response(self):
        """
            Verifies that response thread is still running when the output stream has nothing
            This simulates a subprocess not outputting to it's std out immediately
        """
        input_stream = BytesIO()
        output_stream = BytesIO()

        test_client = Rpc_Client(input_stream, output_stream)
        test_client.start()
        
        self.assertTrue(test_client.request_thread.isAlive())
        self.assertTrue(test_client.response_thread.isAlive())
        self.assertEqual(threading.active_count(), 3)

        test_client.shutdown()
        self.assertEqual(threading.active_count(), 1)

    def test_stream_closed_during_process(self):
        """
            Verifies that when a request stream is closed that the request thread enqueues the exception
            and terminates itself by breaking out of it's loop but not issuing the cancel flag.
        """
        input_stream = BytesIO()
        output_stream = BytesIO(b'Content-Length: 15\r\n\r\n{"key":"value"}')

        test_client = Rpc_Client(input_stream, output_stream)
        test_client.start()

        input_stream.close()
        test_client.submit_request('scriptingService/ScriptDatabase', {'ScriptLogins' : 'True'})
        
        exception = test_client.exception_queue.get()

        # Verify the background thread communicated the exception
        self.assertEqual(exception.args, ("I/O operation on closed file.",))
        # Verify the threads are still running
        # Assert that the background thread killed itself witout setting the cancel flag
        self.assertEqual(threading.active_count(), 2)
        self.assertFalse(test_client.cancel)
        test_client.shutdown()

    def shutdown_background_threads(self, test_client):
        """
            Utility test method used for only stopping the background threads while leaving 
            streams open for verification
        """
        test_client.cancel = True   
        test_client.request_queue.put(None)

        test_client.request_thread.join()
        test_client.response_thread.join()
        
if __name__ == '__main__':
    unittest.main()       