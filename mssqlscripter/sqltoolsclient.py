# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import logging
import mssqlscripter.jsonrpc.jsonrpcclient as json_rpc_client
import mssqlscripter.jsonrpc.contracts.scriptingservice as scripting

logger = logging.getLogger(u'mssqlscripter.sqltoolsclient')


class SqlToolsClient(object):
    """
        Create sql tools service requests.
    """

    def __init__(self, input_stream, output_stream):
        """
            Initializes the sql tools client.
        """
        self.current_id = 1
        self.json_rpc_client = json_rpc_client.JsonRpcClient(
            input_stream, output_stream)
        self.json_rpc_client.start()

        logger.info(u'Sql Tools Client Initialized')

    def create_request(self, request_type, parameters):
        """
            Create request of request type passed in.
        """
        request = None
        if request_type == u'scripting_request':
            request = scripting.ScriptingRequest(
                self.current_id, self.json_rpc_client, parameters)
            logger.info(
                u'Scripting request id: {} created.'.format(
                    self.current_id))
            self.current_id += 1

            return request

    def shutdown(self):
        logger.info(u'Shutting down Sql Tools Client')
        self.json_rpc_client.shutdown()
