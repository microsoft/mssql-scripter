# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from common.json_rpc import Json_Rpc_Reader
from common.json_rpc import Json_Rpc_Writer
from threading import Thread

import Queue

class Json_Rpc_Client(object):
    """
        This class maintains the responsibilities of orchestrating the async read and write process with json rpc protocol 
        by using background threads.

        The two main threads are the request and response threads which operate on the background and sole responsibility is
        to enqueue requests and read/enqueue responses respectively.

        This class provides a shutdown method to ensure resources are released/closed properly.
    """

    REQUEST_THREAD_NAME = 'Request_Thread'
    RESPONSE_THREAD_NAME = 'Response_Thread'

    def __init__(self, in_stream, out_stream):
        self.writer = Json_Rpc_Writer(in_stream)
        self.reader = Json_Rpc_Reader(out_stream)

        self.request_queue = Queue.Queue()
        self.response_queue = Queue.Queue()
        self.exception_queue = Queue.Queue()

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
        """
        if (method is None or params is None):
            return False

        request = {'method' : method, 'params' : params, 'id' : id}
        self.request_queue.put(request)            
        return True

    
    def get_response(self):
        """
            Retrieves the latest response from the queue. Clients will use this method to get the latest response from the stream.
            If a exception occured from either of the threads, we throw the earliest exception.
        """
        if (not self.exception_queue.empty()):
            ex = self.exception_queue.get()
            raise ex
        
        if (not self.response_queue.empty()):
            response = self.response_queue.get()
            return response
        
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
                # Enqueue the response
                self.response_queue.put(response)
               
            except EOFError:
                # Nothing was read from stream, keep trying
                pass
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

    def _record_exception(self, ex, thread_name, logger=None):
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

        # Wait for threads to finish with a timeout
        self.request_thread.join(0.2)
        self.response_thread.join(0.2)

        # close the underlying readers and writers
        self.reader.close()
        self.writer.close()