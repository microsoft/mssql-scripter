# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import mssql.common.jsonrpc as json_rpc
import logging
from queue import Queue
import threading

logger = logging.getLogger(u'mssql-scripter.common.json_rpc_client')


class JsonRpcClient(object):
    """
        Handle async request submission with async response handling.
    """

    REQUEST_THREAD_NAME = u'Json_Rpc_Request_Thread'
    RESPONSE_THREAD_NAME = u'Json_Rpc_Response_Thread'

    def __init__(self, in_stream, out_stream):
        self.writer = json_rpc.JsonRpcWriter(in_stream)
        self.reader = json_rpc.JsonRpcReader(out_stream)

        self.request_queue = Queue()
        # Response map intialized with event queue.
        self.response_map = {0: Queue()}
        self.exception_queue = Queue()

        self.cancel = False

    def start(self):
        """
            Starts the background threads to listen for responses and requests from the underlying
            streams. Encapsulated into it's own method for future async extensions without threads.
        """
        self.request_thread = threading.Thread(
            target=self._listen_for_request,
            name=self.REQUEST_THREAD_NAME)
        self.request_thread.daemon = True
        self.request_thread.start()

        self.response_thread = threading.Thread(
            target=self._listen_for_response,
            name=self.RESPONSE_THREAD_NAME)
        self.response_thread.daemon = True
        self.response_thread.start()

    def submit_request(self, method, params, id=None):
        """
            Submit json rpc request to input stream.
        """
        if (method is None or params is None):
            raise ValueError(u'Method or Parameter was not found in request')

        request = {u'method': method, u'params': params, u'id': id}
        self.request_queue.put(request)

    def request_finished(self, id):
        """
            Remove request id response entry.
        """
        if id in self.response_map:
            del self.response_map[id]

    def get_response(self, id=0):
        """
            Get latest response. Priority order: Response, Event, Exception.
        """
        if id in self.response_map:
            if not self.response_map[id].empty():
                return self.response_map[id].get()

        if not self.response_map[0].empty():
            return self.response_map[0].get()

        if not self.exception_queue.empty():
            raise self.exception_queue.get()

        return None

    def _listen_for_request(self):
        """
            Submit request if available.
        """
        while not self.cancel:
            try:
                # Block until queue contains a request.
                request = self.request_queue.get()

                if request:
                    self.writer.send_request(
                        method=request[u'method'],
                        params=request[u'params'],
                        id=request[u'id'])

            except ValueError as error:
                # Stream is closed, break out of the loop.
                self._record_exception(error, self.REQUEST_THREAD_NAME)
                break
            except Exception as error:
                # Catch generic exceptions.
                self._record_exception(error, self.REQUEST_THREAD_NAME)
                break

    def _listen_for_response(self):
        """
            Listen for and store response, event or exception for main thread to access.
            Exceptions:
                ValueError
                    The stream was closed. Exit the thread immediately.
                LookupError
                    No valid header with content-length was found.
                EOFError
                    The stream may not contain any bytes yet, so retry.
        """
        while not self.cancel:
            try:
                response = self.reader.read_response()
                response_id_str = response.get(u'id')
                if response_id_str:
                    response_id = int(response_id_str)
                    # we have a id, map it with a new queue if it doesn't
                    # exist.
                    if response_id not in self.response_map:
                        self.response_map[response_id] = Queue()
                    # Enqueue the response.
                    self.response_map[response_id].put(response)
                else:
                    # Event was returned.
                    self.response_map[0].put(response)

            except EOFError as error:
                # Thread fails once we reach EOF.
                self._record_exception(error, self.RESPONSE_THREAD_NAME)
                break
            except ValueError as error:
                # Stream was closed.
                self._record_exception(error, self.RESPONSE_THREAD_NAME)
                break
            except LookupError as error:
                # Content-Length header was not found.
                self._record_exception(error, self.RESPONSE_THREAD_NAME)
                break
            except Exception as error:
                # Catch generic exceptions.
                self.record_exception(error, self.RESPONSE_THREAD_NAME)
                break

    def _record_exception(self, ex, thread_name):
        """
            Record exception to allow main thread to access.
        """
        logger.debug(
            u'Thread: {} encountered exception {}'.format(
                thread_name, ex))
        self.exception_queue.put(ex)

    def shutdown(self):
        """
            Signal request thread to close as soon as it can.
        """
        self.cancel = True
        # Enqueue None to optimistically unblock background threads so
        # they can check for the cancellation flag.
        self.request_queue.put(None)

        # Wait for request thread to finish with a timeout in seconds.
        self.request_thread.join(0.2)

        # close the underlying writer.
        self.writer.close()
