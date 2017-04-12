# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
from __future__ import division
import enum
import json
import logging


logger = logging.getLogger(u'mssql-scripter.common.json_rpc')


class ReadState(enum.Enum):
    Header = 1
    Content = 2


class JsonRpcWriter(object):
    """
        Write JSON RPC message to input stream.
    """
    HEADER = u'Content-Length: {0}\r\n\r\n'

    def __init__(self, stream, encoding=None):
        self.stream = stream
        self.encoding = encoding or u'UTF-8'

    def send_request(self, method, params, id=None):
        """
        Send JSON RPC request message.
        Exceptions raised:
            ValueError
                If the stream was closed externally.
        """
        # Perhaps move to a different def to add some validation
        content_body = {
            u'jsonrpc': u'2.0',
            u'method': method,
            u'params': params,
            u'id': id
        }

        json_content = json.dumps(content_body, sort_keys=True)
        header = self.HEADER.format(str(len(json_content)))
        try:
            self.stream.write(header.encode(u'ascii'))
            self.stream.write(json_content.encode(self.encoding))
            self.stream.flush()

        except ValueError as ex:
            logger.debug(u'Send Request encountered exception {}'.format(ex))
            raise ex

    def close(self):
        """
            Close the stream.
        """
        try:
            self.stream.close()
        except AttributeError:
            pass


class JsonRpcReader(object):
    """
        Read JSON RPC message from output stream.
    """
    # \r\n
    CR = 13
    LF = 10
    BUFFER_RESIZE_TRIGGER = 0.25
    DEFAULT_BUFFER_SIZE = 8192

    def __init__(self, stream, encoding=None):
        self.encoding = encoding or u'UTF-8'

        self.stream = stream
        self.buffer = bytearray(self.DEFAULT_BUFFER_SIZE)
        # Pointer to end of buffer content.
        self.buffer_end_offset = 0
        # Pointer to where we have read up to.
        self.read_offset = 0
        self.expected_content_length = 0
        self.headers = {}
        self.read_state = ReadState.Header
        self.needs_more_data = True

    def read_response(self):
        """
            Read JSON RPC message from buffer.
        Exceptions raised:
            ValueError
                if the body-content can not be serialized to a JSON object.
        """
        # Using a mutable list to hold the value since a immutable string
        # passed by reference won't change the value.
        content = ['']
        try:
            while (not self.needs_more_data or self.read_next_chunk()):
                # We should have all the data we need to form a message in the buffer.
                # If we need more data to form the next message, this flag will
                # be reset by a attempt to form a header or content.
                self.needs_more_data = False
                # If we can't read a header, read the next chunk.
                if self.read_state is ReadState.Header and not self.try_read_headers():
                    self.needs_more_data = True
                    continue
                # If we read the header, try the content. If that fails, read
                # the next chunk.
                if self.read_state is ReadState.Content and not self.try_read_content(
                        content):
                    self.needs_more_data = True
                    continue
                # We have the  content
                break

            # Resize buffer and remove bytes we have read
            self.trim_buffer_and_resize(self.read_offset)
            return json.loads(content[0])
        except ValueError as ex:
            # response has invalid json object.
            logger.debug(
                u'JSON RPC Reader on read_response() encountered exception: {}'.format(ex))
            raise ex

    def read_next_chunk(self):
        """
        Read a chunk from the output stream into buffer.
        Exceptions raised:
            EOFError
                Stream was empty or Stream did not contain a valid header or content-body.
            ValueError
                Stream was closed externally.
        """
        # Check if we need to resize.
        current_buffer_size = len(self.buffer)
        if ((current_buffer_size - self.buffer_end_offset) /
                current_buffer_size) < self.BUFFER_RESIZE_TRIGGER:
            resized_buffer = bytearray(current_buffer_size * 2)
            # copy current buffer content to new buffer.
            resized_buffer[0:current_buffer_size] = self.buffer
            # point to new buffer.
            self.buffer = resized_buffer

        # Memory view is required in order to read into a subset of a byte
        # array
        try:
            length_read = self.stream.readinto(
                memoryview(self.buffer)[self.buffer_end_offset:])
            self.buffer_end_offset += length_read

            if not length_read:
                logger.debug(u'JSON RPC Reader reached end of stream')
                raise EOFError(u'End of stream reached, no output.')

            return True
        except ValueError as ex:
            logger.debug(
                u'JSON RPC Reader on read_next_chunk encountered exception: {}'.format(ex))
            # Stream was closed.
            raise ex

    def try_read_headers(self):
        """
        Try to read the Header information from the internal buffer expecting the last header to contain '\r\n\r\n'.
        Exceptions:
            LookupError
                The content-length header was not found.
            ValueError
                The content-length contained a invalid literal for int.
        """
        # Scan the buffer up until right before the CRLFCRLF.
        scan_offset = self.read_offset
        while (scan_offset + 3 < self.buffer_end_offset and
                (self.buffer[scan_offset] != self.CR or
                 self.buffer[scan_offset + 1] != self.LF or
                 self.buffer[scan_offset + 2] != self.CR or
                 self.buffer[scan_offset + 3] != self.LF)):
            scan_offset += 1

        # if we reached the end
        if scan_offset + 3 >= self.buffer_end_offset:
            return False

        # Split the headers by new line
        try:
            headers_read = self.buffer[self.read_offset:scan_offset].decode(
                u'ascii')
            for header in headers_read.split(u'\n'):
                colon_index = header.find(u':')

                if colon_index == -1:
                    logger.debug(
                        u'JSON RPC Reader encountered missing colons in try_read_headers()')
                    raise KeyError(
                        u'Colon missing from Header: {}.'.format(header))

                # Case insensitive.
                header_key = header[:colon_index].lower()
                header_value = header[colon_index + 1:]

                self.headers[header_key] = header_value

            # Was content-length header found?
            if not ('content-length' in self.headers):
                logger.debug(
                    u'JSON RPC Reader did not find Content-Length in the headers')
                raise LookupError(
                    u'Content-Length was not found in headers received.')

            self.expected_content_length = int(self.headers[u'content-length'])

        except ValueError:
            # Content-length contained invalid literal for int.
            self.trim_buffer_and_resize(scan_offset + 4)
            raise

        # Pushing read pointer past the newline characters.
        self.read_offset = scan_offset + 4
        self.read_state = ReadState.Content

        return True

    def try_read_content(self, content):
        """
            Try to read content from internal buffer.
        """
        if (self.buffer_end_offset - self.read_offset <
                self.expected_content_length):
            # We buffered less than the expected content length.
            return False

        content[0] = self.buffer[self.read_offset:self.read_offset +
                                 self.expected_content_length].decode(self.encoding)
        self.read_offset += self.expected_content_length

        self.read_state = ReadState.Header

        return True

    def trim_buffer_and_resize(self, bytes_to_remove):
        """
        Trim the buffer by the passed in bytes_to_remove by creating a new buffer that is at a minimum the default max size.
        """
        current_buffer_size = len(self.buffer)
        # Create a new buffer with either minumum size or leftover size.
        new_buffer = bytearray(max(current_buffer_size -
                                   bytes_to_remove, self.DEFAULT_BUFFER_SIZE))

        # if we have content we did not read, copy that portion to the new
        # buffer.
        if (bytes_to_remove <= current_buffer_size):
            new_buffer[:self.buffer_end_offset -
                       bytes_to_remove] = self.buffer[bytes_to_remove:self.buffer_end_offset]

        # Point to the new buffer.
        self.buffer = new_buffer

        # reset pointers after the shift.
        self.read_offset = 0
        self.buffer_end_offset -= bytes_to_remove

    def close(self):
        """
            Close the stream.
        """
        try:
            self.stream.close()
        except AttributeError:
            pass
