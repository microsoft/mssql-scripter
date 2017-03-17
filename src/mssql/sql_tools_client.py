# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from common.json_rpc_client import Json_Rpc_Client

class Sql_Tools_Client(object):
    """
        Main client that each CLI interacts with. Wraps around the json rpc client.
        Has knowledge of each command sql tools service supports.
            Each command itself knows how to handle it's own life cycle and expected types
    """
    def __init__(self, intput_stream, output_stream):
        """
            Initializes the client with the json rpc client hooked up to the streams
        """
        self.json_rpc_client = Json_Rpc_Client(input_stream, output_stream)

    def create_command_factory(command_type, parameters):
        """
            Factory method to create the specified command with the passed in type.
            Command is initialized with the rpc client within it.
        """
        pass


"""
    TODO: Current design thought starting from lowest level

    Commands
        Handle it's own lifecycle from execute, stop, shutdown, get response, and state reporting.
            Requests and responses will be serialized/deserialized via JSON Pickle.
            The Request and event types will be defined in it's own class all top level subclassing from object.
                Why? removes redundancy if a different commands may require the same type of event since it can nest calls to the service
    Tools Service client:
        For now will be all knowing and all cli tools will have to interact with this client.

    Extension story:
        Create your new command.
        Create your new event and response and request with it's own serializing/deserializing declaration.
        Wire up the command to the factory method in sql tools client
        Create your main.py to interact with the tools client

    Future with multiple different commands sent to the tools service:
        We will require a dispatching layer in between the command and the rpc client to handle the case where multiple commands are executing and
        the response queue in json rpc client is populated with multiple types of events mapped to different commands.

        Dispatcher will pull latest response from event queue in rpc client and dispatch to the registered handlers or 
        each command has it's own queue of responses so that the main thread can access immediately.

        Tools client will have to maintain a map between commands and handlers?

        Dispatcher may work on background thread

"""