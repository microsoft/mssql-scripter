# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from common.json_rpc import Json_Rpc_Reader
from common.json_rpc import Json_Rpc_Writer
from threading import Thread

import Queue
import time

class Rpc_Client(object):
    """
        This class maintains the responsibilities of orchestrating the read and write process using the json rpc protocl.
        It maintains thread safe queues that all different background threads to handle each request and response.

        Two main threads are the request and response threads which operate on the background and who's sole responsibility is
        to enqueue requests and read/enqueue responses.

        This class provides a shutdown method to ensure resources are released/closed properly.

        Accompanied with this class are unit tests that test a decent amount of the scenario but require more gritty 
        test cases regarding the threads.

        this class maintains a exceptions queue that is meant to be used as cross thread communication. This queue needs to 
        be updated to contain more verbose information. The current state assumes that any ValueError exception found in the exception
        queue requires the caller to shut down the process as the thread that enqueued in is not able to process with a closed stream.
    """
    def __init__(self, in_stream, out_stream):
        self.writer = Json_Rpc_Writer(in_stream)
        self.reader = Json_Rpc_Reader(out_stream)

        self.request_queue = Queue.Queue()
        self.response_queue = Queue.Queue()
        # Exceptions that can occur during background threads occur here.
        # It is the callers responsibilities to check this queue
        # TODO: Refine content put into the queue with the executing threads name
        self.exception_queue = Queue.Queue()

        # Simple cancellation token boolean
        self.cancel = False

    def start(self):
        """
            Starts the background threads to listen for responses and requests from the underlying 
            streams. Encapsulated into it's own method for future async extensions without threads.
        """
        #TODO: Give a name to each thread
        self.request_thread = Thread(target = self._listen_for_request)
        self.request_thread.daemon = True
        self.request_thread.start()
        
        self.response_thread = Thread(target = self._listen_for_response)
        self.response_thread.daemon = True
        self.response_thread.start()

    def submit_request(self, method, params, id = None):
        """
            Enqueue's the request
        """
        
        if (method is None or params is None):
            return False

        request = {'method' : method, 'params' : params, 'id' : id}
        self.request_queue.put(request)            
        return True

    def _listen_for_request(self):
        """
            Dequeue's the first request and writes the request.
            Exceptions:
                IOError: we continue on IO errors since the scenario where the stream may not have data immediately
                         is valid
                ValueError:
                         The stream was closed externally. We log the exception into the queue for the main thread to check
                         and kill the thread since it won't be able to proceed with a closed stream
        """
        while(not self.cancel):
            try:
                # Calling a blocking get on the queue keeps CPU usage at a 
                # minimum versus non blocking or with a timeout
                request = self.request_queue.get()
                
                if (not request is None):
                    #print(request)
                    self.writer.send_request(method=request['method'], params=request['params'], id=request['id'])
            except IOError:
                pass
            except ValueError as error:
                # Stream is closed, break out of the loop
                # TODO refine this so the caller knows which thread the exception occured in
                self.exception_queue.put(error)
                break

    def _listen_for_response(self):
        """
            Listens for response from stream and enqueue's the response.
            Client is responsibile for dequeuing and dispatching/handling each response
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
                self.exception_queue.put(error)
                raise
            except LookupError as error:
                # Content-Length header was not found
                self.exception_queue.put(error)
                raise

    def shutdown(self):
        """
            Signals to the threads to close after handling it's request/response
        """
        self.cancel = True
        # Enqueue None to optimistically unblock background threads so 
        # they can check for the cancellation flag
        self.request_queue.put(None)

        # Wait for threads to finish
        self.request_thread.join()
        self.response_thread.join()

        # close the underlying readers and writers
        self.reader.close()
        self.writer.close()