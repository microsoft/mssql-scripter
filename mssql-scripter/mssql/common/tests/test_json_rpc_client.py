# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import mssql.common.json_rpc_client as json_rpc_client
import unittest
import threading
import time
import io

class Json_Rpc_Client_Tests(unittest.TestCase):

    def test_request_enqueued(self):
        """
            Test that verifies requests sent to the json rpc client are enqueued succesfully.
        """
        input_stream = io.BytesIO()
        output_stream = io.BytesIO(b'sample output')

        test_client = json_rpc_client.Json_Rpc_Client(input_stream, output_stream)
        test_client.submit_request(
            'scriptingService/ScriptDatabase', {'ScriptDatabaseOptions': 'True'})

        request = test_client.request_queue.get()

        self.assertEqual(request['method'], 'scriptingService/ScriptDatabase')
        self.assertEqual(request['params'], {'ScriptDatabaseOptions': 'True'})

    def test_response_dequeued(self):
        """
            Test that verifies a response was successfully read/enqueued and dequeued from the response queue.
        """
        input_stream = io.BytesIO()
        output_stream = io.BytesIO(b'Content-Length: 15\r\n\r\n{"key":"value"}')

        test_client = json_rpc_client.Json_Rpc_Client(input_stream, output_stream)
        test_client.start()

        self.shutdown_background_threads(test_client)

        response = test_client.get_response()
        baseline = {"key": "value"}

        self.assertEqual(response, baseline)
        # All background threads should be shut down
        self.assertFalse(test_client.request_thread.isAlive())
        self.assertFalse(test_client.response_thread.isAlive())
        self.assertEqual(threading.active_count(), 1)

    def test_submit_simple_request(self):
        """
            Verifies that we are able to submit a request successfully via the json rpc client.
        """
        input_stream = io.BytesIO()
        output_stream = io.BytesIO(b'Content-Length: 15\r\n\r\n{"key":"value"}')

        test_client = json_rpc_client.Json_Rpc_Client(input_stream, output_stream)
        test_client.start()

        # Verify threads are alive and running
        self.assertTrue(test_client.request_thread.isAlive())
        self.assertFalse(test_client.response_thread.isAlive())
        self.assertEqual(threading.active_count(), 2)

        test_client.submit_request(
            'scriptingService/ScriptDatabase', {'ScriptDatabaseOptions': 'True'})

        self.shutdown_background_threads(test_client)

        # check stream contents
        input_stream.seek(0)
        expected = b'Content-Length: 120\r\n\r\n{"id": null, "jsonrpc": "2.0", "method": "scriptingService/ScriptDatabase", "params": {"ScriptDatabaseOptions": "True"}}'

        self.assertEqual(input_stream.getvalue(), expected)
        self.assertFalse(test_client.request_thread.isAlive())
        self.assertFalse(test_client.response_thread.isAlive())
        self.assertEqual(threading.active_count(), 1)

    def test_send_multiple_request(self):
        """
            Verifies we can successfully submit multiple requests.
        """
        input_stream = io.BytesIO()
        output_stream = io.BytesIO(b'Content-Length: 15\r\n\r\n{"key":"value"}')

        test_client = json_rpc_client.Json_Rpc_Client(input_stream, output_stream)
        test_client.start()

        # Verify request thread is up and running and response thread is dead
        # since it should have reached EOF.
        self.assertTrue(test_client.request_thread.isAlive())
        self.assertFalse(test_client.response_thread.isAlive())
        self.assertEqual(threading.active_count(), 2)

        test_client.submit_request(
            'scriptingService/ScriptDatabase', {'ScriptDatabaseOptions': 'True'})
        test_client.submit_request(
            'scriptingService/ScriptDatabase', {'ScriptCollations': 'True'})
        test_client.submit_request(
            'scriptingService/ScriptDatabase', {'ScriptDefaults': 'True'})

        # Minimum sleep time for main thread so background threads can process
        # the requests.
        time.sleep(1)

        # Kill the threads so we can just verify the queues
        self.shutdown_background_threads(test_client)

        input_stream.seek(0)
        expected = \
            b'Content-Length: 120\r\n\r\n{"id": null, "jsonrpc": "2.0", "method": "scriptingService/ScriptDatabase", "params": {"ScriptDatabaseOptions": "True"}}'\
            b'Content-Length: 115\r\n\r\n{"id": null, "jsonrpc": "2.0", "method": "scriptingService/ScriptDatabase", "params": {"ScriptCollations": "True"}}'\
            b'Content-Length: 113\r\n\r\n{"id": null, "jsonrpc": "2.0", "method": "scriptingService/ScriptDatabase", "params": {"ScriptDefaults": "True"}}'

        self.assertEqual(input_stream.getvalue(), expected)
        self.assertFalse(test_client.request_thread.isAlive())
        self.assertFalse(test_client.response_thread.isAlive())
        self.assertEqual(threading.active_count(), 1)

    def test_normal_shutdown(self):
        """
            Verifies we can gracefully shutdown.
        """
        input_stream = io.BytesIO()
        output_stream = io.BytesIO(b'Content-Length: 15\r\n\r\n{"key":"value"}')

        test_client = json_rpc_client.Json_Rpc_Client(input_stream, output_stream)
        test_client.start()

        # Verify threads are alive and running
        self.assertTrue(test_client.request_thread.isAlive())
        self.assertEqual(threading.active_count(), 2)

        # Response thread should have reach EOF during test execution which
        # should end the response thread.
        self.assertFalse(test_client.response_thread.isAlive())

        test_client.shutdown()

        self.assertFalse(test_client.request_thread.isAlive())
        self.assertFalse(test_client.response_thread.isAlive())
        self.assertEqual(threading.active_count(), 1)

    def test_send_invalid_request(self):
        """
            Verifies that a request with a null method or parameter is not enqueued.
        """
        input_stream = io.BytesIO()
        output_stream = io.BytesIO(b'sample output')

        test_client = json_rpc_client.Json_Rpc_Client(input_stream, output_stream)
        with self.assertRaises(ValueError):
            test_client.submit_request(None, None)

    def test_receive_invalid_response_exception(self):
        """
            Verifies that when a invalid response is read, the response thread enqueues the Exception
            into the exception queue for the main thread to access and kills itself.
        """
        input_stream = io.BytesIO()
        output_stream = io.BytesIO(b'Cntent-Lenth:15\r\n\r\n')

        test_client = json_rpc_client.Json_Rpc_Client(input_stream, output_stream)
        test_client.start()

        try:
            # Retrieve the latest response or earliest exception
            test_client.get_response()
        except LookupError as exception:
            # Verify the background thread communicated the exception
            self.assertEqual(
                exception.args, ('Content-Length was not found in headers received.',))
            # Expect a look up error exception since the content-length is not
            # found
            self.assertTrue(test_client.request_thread.isAlive())
            self.assertFalse(test_client.response_thread.isAlive())
            self.assertEqual(threading.active_count(), 2)
            test_client.shutdown()
            self.assertEqual(threading.active_count(), 1)

    def test_response_stream_closed_exception(self):
        """
            Verifies that when the response stream is closed that the proper exception is enqueued and that the worker thread
            killed itself.
        """
        input_stream = io.BytesIO()
        output_stream = io.BytesIO(b'Content-Lenth:15\r\n\r\n')
        output_stream.close()

        test_client = json_rpc_client.Json_Rpc_Client(input_stream, output_stream)
        test_client.start()

        try:
            test_client.get_response()
        except ValueError as exception:
             # Verify the background thread communicated the exception
            self.assertEqual(
                exception.args, ("I/O operation on closed file.",))
            # Expecting a Value error as we are attempting to access a closed
            # stream.
            self.assertTrue(test_client.request_thread.isAlive())
            self.assertFalse(test_client.response_thread.isAlive())
            self.assertEqual(threading.active_count(), 2)
            test_client.shutdown()
            self.assertEqual(threading.active_count(), 1)

    @unittest.skip("Disabling until scenario is valid")
    def test_stream_has_no_response(self):
        """
            Verifies that response thread is still running when the output stream has nothing
            This simulates a subprocess not outputting to it's std out immediately.
        """
        input_stream = io.BytesIO()
        output_stream = io.BytesIO()

        test_client = json_rpc_client.Json_Rpc_Client(input_stream, output_stream)
        test_client.start()
        response = test_client.get_response()

        self.assertEqual(response, None)
        self.assertTrue(test_client.request_thread.isAlive())
        self.assertTrue(test_client.response_thread.isAlive())
        self.assertEqual(threading.active_count(), 3)

        test_client.shutdown()
        self.assertEqual(threading.active_count(), 1)

    def test_stream_closed_during_process(self):
        """
            Verifies that when a request stream is closed that the request thread enqueues the exception
            and terminates itself by breaking out of it's loop.
        """
        input_stream = io.BytesIO()
        output_stream = io.BytesIO(b'Content-Length: 15\r\n\r\n{"key":"value"}')

        test_client = json_rpc_client.Json_Rpc_Client(input_stream, output_stream)
        test_client.start()
        input_stream.close()
        test_client.submit_request(
            'scriptingService/ScriptDatabase', {'ScriptLogins': 'True'})
        # Minimum sleep time to give the request thread time to process the
        # request.
        time.sleep(1)

        try:
            test_client.get_response()
        except ValueError as exception:
            # Verify the background thread communicated the exception
            self.assertEqual(
                exception.args, ("I/O operation on closed file.",))
            # Verify the response thread is dead
            self.assertFalse(test_client.request_thread.isAlive())
            self.assertEqual(threading.active_count(), 1)
            test_client.shutdown()

    def test_get_response_with_id(self):
        """
            Tests that get response with id can return either a response associated with a id or a event with no id
        """
        input_stream = io.BytesIO()
        output_stream = io.BytesIO(
            b'Content-Length: 86\r\n\r\n{"params": {"Key": "Value"}, "jsonrpc": "2.0", "method": "testMethod/DoThis", "id": 1}')

        test_client = json_rpc_client.Json_Rpc_Client(input_stream, output_stream)
        test_client.start()

        # Sleeping to give background threads a chance to process response.
        time.sleep(1)

        baseline = {
            "jsonrpc": "2.0",
            "params": {
                "Key": "Value"},
            "method": "testMethod/DoThis",
            "id": 1}
        response = test_client.get_response(1)
        self.assertEqual(response, baseline)
        test_client.shutdown()

    def shutdown_background_threads(self, test_client):
        """
            Utility test method used for only stopping the background threads while leaving
            streams open for verification.
        """
        test_client.cancel = True
        test_client.request_queue.put(None)

        test_client.request_thread.join()
        test_client.response_thread.join()


if __name__ == '__main__':
    unittest.main()
