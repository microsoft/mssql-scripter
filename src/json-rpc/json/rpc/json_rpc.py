# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from io import BytesIO
import json

class JSON_RPC_Writer(object):
    HEADER = "Content-Length: {0}\r\n\r\n"
    
    def __init__(self, stream, encoding = None):
        self.stream = stream
        self.encoding = encoding
        if encoding is None:
            self.encoding = 'UTF-8'

    def send_request(self, method, params, id):
        # Perhaps move to a different def to add some validation
        content_body = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": id 
        }

        json_content = json.dumps(content_body)
        header = self.HEADER.format(str(len(json_content)))

        self.stream.write(header.encode("ascii"))
        self.stream.write(json_content.encode(self.encoding))

class JSON_RPC_Reader(object):
    # \r\n
    CR = 13
    LF = 10
    BUFFER_RESIZE_TRIGGER= 0.25
    DEFAULT_BUFFER_SIZE = 8192

    def __init__(self, stream, encoding = None):
        self.encoding = encoding
        if encoding is None:
            self.encoding = 'UTF-8'

        self.stream = stream
        self.buffer = bytearray(self.DEFAULT_BUFFER_SIZE)       
        # Pointer to end of buffer content
        self.buffer_end_offset = 0
        # Pointer to where we have read up to
        self.read_offset = 0
        self.expected_content_length = 0
        self.headers = {}
        #TODO: Create enum
        self.read_state = "Header"

    def read_response(self):
        # Using a mutable list to hold the value since a immutable string passed by reference won't change the value
        message_content = [""]
        while (self.read_next_chunk()):
            # If we can't read a header, read the next chunk
            if (self.read_state == "Header" and not self.try_read_message_headers()):
                continue
            # If we read the header, try the content. If that fails, read the next chunk
            if (self.read_state == "Content" and not self.try_read_message_content(message_content)):
                continue
            # We have the message content
            break
        
        # Resize buffer and remove bytes we have read
        self.shift_buffer_bytes_and_reset(self.read_offset)
        try:
            return json.loads(message_content[0])
        except ValueError as error:
            # response has invalid json object, throw Exception TODO: log message
            raise

    def read_next_chunk(self):
        # Check if we need to resize
        current_buffer_size = len(self.buffer)
        if ((current_buffer_size - float(self.buffer_end_offset)) / current_buffer_size) < self.BUFFER_RESIZE_TRIGGER:
            resized_buffer = bytearray(current_buffer_size * 2)
            # copy current buffer content to new buffer
            resized_buffer[0:current_buffer_size] = self.buffer
            # point to new buffer
            self.buffer = resized_buffer

        # read next chunk into buffer
        # Memory view is required in order to read into a subset of a byte array
        try:
            length_read = self.stream.readinto(memoryview(self.buffer)[self.buffer_end_offset:])
            self.buffer_end_offset += length_read

            if (length_read == 0):
                # Nothing was read, could be due to the server process shutting down while leaving stream open
                # close stream and return false and/or throw exception?
                # for now throwing exception
                raise EOFError("End of stream reached with no valid header or content-body")

            return True

        except Exception:
            #TODO: Add more granular exception message 
            raise

    def try_read_message_headers(self):
        # Scan the buffer up until right before the CRLFCRLF
        scan_offset = self.read_offset
        while(scan_offset + 3 < self.buffer_end_offset and
                (self.buffer[scan_offset] != self.CR or
                self.buffer[scan_offset + 1] != self.LF or
                self.buffer[scan_offset + 2] != self.CR or
                self.buffer[scan_offset + 3] != self.LF)):
            scan_offset += 1
            
        # if we reached the end
        if (scan_offset + 3 >= self.buffer_end_offset ):
            return False

        # Split the headers by new line
        try:
            headers_read = self.buffer[self.read_offset:scan_offset].decode('ascii').split('\n')
            for header in headers_read:
                colon_index = header.find(':')

                if (colon_index == -1):
                    raise KeyError("Colon missing from Header")
                
                header_key = header[:colon_index]
                header_value = header[colon_index + 1:]

                self.headers[header_key] = header_value
            
            #Find content body in the list of headers and parse the Value
            if (self.headers["Content-Length"] is None):
                raise LookupError("Content Length was not found in headers received")
            
            self.expected_content_length = int(self.headers["Content-Length"])

        except Exception:
            # Trash the buffer we read and shift past read content
            self.shift_buffer_bytes_and_reset(self.scan_offset + 4)
            raise

        # Pushing read pointer past the newline characters
        self.read_offset = scan_offset + 4
        # TODO: Create enum for this
        self.read_state = "Content"
        return True

    def try_read_message_content(self, message_content):
        # if we buffered less than the expected content length, return false
        if (self.buffer_end_offset - self.read_offset < self.expected_content_length):
            return False

        message_content[0] = self.buffer[self.read_offset:self.read_offset + self.expected_content_length].decode(self.encoding)
        self.read_offset += self.expected_content_length
        #TODO: Create a enum for this
        self.read_state = "Header"
        return True
        
    def shift_buffer_bytes_and_reset(self, bytes_to_remove):
        current_buffer_size = len(self.buffer)
        # Create a new buffer with either minumum size or leftover size
        new_buffer = bytearray(max(current_buffer_size - bytes_to_remove, self.DEFAULT_BUFFER_SIZE))

        # if we have content we did not read, copy that portion to the new buffer
        if (bytes_to_remove <= current_buffer_size):
            new_buffer[:self.buffer_end_offset - bytes_to_remove] = self.buffer[bytes_to_remove:self.buffer_end_offset]

        # Point to the new buffer
        self.buffer = new_buffer

        # reset pointers after the shift
        self.read_offset = 0
        self.buffer_end_offset -= bytes_to_remove
