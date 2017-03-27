# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from common.json_rpc import Json_Rpc_Reader, Json_Rpc_Writer
from threading import Thread

from queue import Queue

class Json_Rpc_Client(object):
    """
        This class maintains the responsibilities of orchestrating the async read and write process with json rpc protocol 
        by using background threads.

        The two main threads are the request and response threads which operate on the background and sole responsibility is
        to enqueue requests and read/enqueue responses respectively.

        This class provides a shutdown method to ensure resources are released/closed properly.
    """

    REQUEST_THREAD_NAME = 'Json_Rpc_Request_Thread'
    RESPONSE_THREAD_NAME = 'Json_Rpc_Response_Thread'

    def __init__(self, in_stream, out_stream):
        self.writer = Json_Rpc_Writer(in_stream)
        self.reader = Json_Rpc_Reader(out_stream)

        self.request_queue = Queue()
        # Response map intialized with event queue
        self.response_map= {0: Queue()}
        self.exception_queue = Queue()

        # Simple cancellation token boolean
        self.cancel = False

    def start(self):
        """
            Starts the background threads to listen for responses and requests from the underlying 
            streams. Encapsulated into it's own method for future async extensions without threads.
        """
        self.request_thread = Thread(target = self._listen_for_request, name = self.REQUEST_THREAD_NAME)
        self.request_thread.daemon = True
        self.request_thread.start()
        
        self.response_thread = Thread(target = self._listen_for_response, name = self.RESPONSE_THREAD_NAME)
        self.response_thread.daemon = True
        self.response_thread.start()

    def submit_request(self, method, params, id = None):
        """
            Enqueue's the request.
            Exceptions:
                ValueError:
                    Request did not contain a method or parameters
        """
        if (method is None or params is None):
            raise ValueError("Method or Parameter was not found in request")

        request = {'method' : method, 'params' : params, 'id' : id}
        self.request_queue.put(request)    

    def request_finished(self, id):
        """
            Cleans up the response map by removing the passed in id's entry.
            Client is responsible for checking when a response is completed and removable.
        """
        if (id in self.response_map):
            del self.response_map[id]

    def get_response(self, id = 0):
        """
            Retrieves the latest response from the queue. 
            First check if a exception occured and throw the latest one.
            Second, by default we return the latest event, otherwise we return the latest response from the passed in id.
        """
        if (not self.exception_queue.empty()):
            ex = self.exception_queue.get()
            raise ex

        if (id in self.response_map):
            if (not self.response_map[id].empty()):
                return self.response_map[id].get()

        return None

    def _listen_for_request(self):
        """
            Dequeue's the first request and writes the request.
            Exceptions:
                ValueError:
                    The stream was closed. Exit the thread immediately.
        """
        while(not self.cancel):
            try:
                # Calling a blocking get on the queue keeps CPU usage at a 
                # minimum versus non blocking or with a timeout
                request = self.request_queue.get()
                
                if (not request is None):
                    self.writer.send_request(method=request['method'], params=request['params'], id=request['id'])

            except ValueError as error:
                # Stream is closed, break out of the loop
                self._record_exception(error, self.REQUEST_THREAD_NAME)
                break

    def _listen_for_response(self):
        """
            Listens for response from stream and enqueue's the response.
            Client is responsibile for dequeuing and dispatching/handling each response.

            Both exceptions below if thrown require the loop to exit.
            Exceptions:
                ValueError 
                    The stream was closed. Exit the thread immediately.
                LookupError 
                    No valid header with content-length was found.
                EOFError 
                    The stream may not contain any bytes yet, so retry.
        """
        while(not self.cancel):
            try:
                response = self.reader.read_response()
                response_id_str = response.get('id')
                if (not response_id_str is None):
                    # response will be returned as a json string, so parse it to int so clients can use a int id
                    response_id = int(response_id_str)
                    # we have a id, map it with a new queue if it doesn't exist
                    if (not response_id in self.response_map):
                        self.response_map[response_id] = Queue()
                    # Enqueue the response
                    self.response_map[response_id].put(response)
                else:
                    # Event was returned
                    self.response_map[0].put(response)

            except EOFError as error:
                # Nothing was read from stream, break out of the loop
                # TODO: Revisit the scenarios where the stream could for a second not have any content in it.
                break
            except ValueError as error:
                # If we get this error it means the stream was closed
                # Place error into queue for main thread to access
                # Callers responsibility to check for thread state
                self._record_exception(error, self.RESPONSE_THREAD_NAME)
                break
            except LookupError as error:
                # Content-Length header was not found
                self._record_exception(error, self.RESPONSE_THREAD_NAME)
                break

    def _record_exception(self, ex, thread_name, logger = None):
        """
            Helper method that enqueues the exception that was thrown into the exception queue.
            Clients can provide a logger to log the exception with the associated thread name for telemetry.
        """
        #TODO If logger is not null, log the exception with the thread NameError
        self.exception_queue.put(ex)

    def shutdown(self):
        """
            Signals to the threads to close after handling it's request/response.
        """
        self.cancel = True
        # Enqueue None to optimistically unblock background threads so 
        # they can check for the cancellation flag
        self.request_queue.put(None)

        # Wait for request thread to finish with a timeout in seconds
        self.request_thread.join(0.2)

        # close the underlying writer
        self.writer.close()
