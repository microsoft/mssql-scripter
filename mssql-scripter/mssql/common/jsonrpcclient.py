# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from queue import Queue

import logging
import threading
import mssql.common.jsonrpc as json_rpc

logger = logging.getLogger(u'mssql-scripter.common.json_rpc_client')


class JsonRpcClient(object):
    """
        Orchestrate read/response and write/request on 2 daemon threads.
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
            start request and response thread for read and write operations.
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
            Enqueue request to be submitted by request thread.
            Exceptions:
                ValueError:
                    Request did not contain a method or parameters
        """
        if not method or not params:
            raise ValueError(u'Method or Parameter was not found in request')

        request = {u'method': method, u'params': params, u'id': id}
        self.request_queue.put(request)

    def request_finished(self, id):
        """
            Remove request id from response map.
        """
        if id in self.response_map:
            del self.response_map[id]

    def get_response(self, id=0):
        """
            Get exception or response associated to the request id.
        """
        if not self.exception_queue.empty():
            ex = self.exception_queue.get()
            raise ex

        if id in self.response_map:
            if not self.response_map[id].empty():
                return self.response_map[id].get()

        return None

    def _listen_for_request(self):
        """
            Submit latest request.
            Exceptions:
                ValueError:
                    The stream was closed. Exit the thread immediately.
        """
        while not self.cancel:
            try:
                # using blocking queue.get() to minimuize cpu usage.
                request = self.request_queue.get()

                if request:
                    self.writer.send_request(
                        method=request[u'method'],
                        params=request[u'params'],
                        id=request[u'id'])

            except ValueError as error:
                # Stream is closed.
                self._record_exception(error, self.REQUEST_THREAD_NAME)
                break

    def _listen_for_response(self):
        """
            Retrieve and enqueue latest response or event.

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
                # Nothing was read from stream, keep listening.
                break
            except ValueError as error:
                # Stream was closed.
                self._record_exception(error, self.RESPONSE_THREAD_NAME)
                break
            except LookupError as error:
                # Content-Length header was not found.
                self._record_exception(error, self.RESPONSE_THREAD_NAME)
                break

    def _record_exception(self, ex, thread_name):
        """
            Record exception.
        """
        logger.debug(
            u'Thread: {} encountered exception {}'.format(
                thread_name, ex))
        self.exception_queue.put(ex)

    def shutdown(self):
        """
            Shut down request thread and queue.
        """
        self.cancel = True
        # Submit none as a request to allow request thread to check for cancel
        # flag.
        self.request_queue.put(None)
        # wait on request thread for 0.2 seconds.
        self.request_thread.join(0.2)
        self.writer.close()

        # Response thread will block and die when main process dies.
