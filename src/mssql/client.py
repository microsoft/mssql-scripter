# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from common.json_rpc_client import Json_Rpc_Client
from mssql.requests.scripting import *

import logging

logger = logging.getLogger('mssql.client')


class Sql_Tools_Client(object):
    """
        Main client that each CLI interacts with. Wraps around the json rpc client.
        Has knowledge of each command sql tools service supports.
            Each command itself knows how to handle it's own life cycle and expected types
    """

    def __init__(self, input_stream, output_stream):
        """
            Initializes the client with the json rpc client hooked up to the streams
        """
        self.current_id = 1
        self.json_rpc_client = Json_Rpc_Client(input_stream, output_stream)
        self.json_rpc_client.start()

        logger.info('Sql Tools Client Initialized')

    def create_request_factory(self, request_type, parameters):
        """
            Factory method to create the specified command with the passed in type.
            Command is initialized with the rpc client within it.
        """
        request = None
        if (request_type == 'scripting_request'):
            request = Scripting_Request(
                self.current_id, self.json_rpc_client, parameters)
            logger.info(
                'Scripting request id: {0} created.'.format(
                    self.current_id))
            self.current_id += 1

            return request

    def shutdown(self):
        logger.info('Shutting down Sql Tools Client')
        self.json_rpc_client.shutdown()
