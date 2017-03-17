# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------


from abc import abstractmethod

class Command(object):
    """
        Abstract command class that all service commands need to subclass.
        Each commands responsibilities:
             Method name in the sql tools service
             Typed parameters
             Serialization and Deserialization of it's Typed response and events
            
    """
    def __init__(self, rpc_client, parameters):
        self.rpc_client = rpc_client
        # Parameters will be typed, so when submitting request we need to serialize them
        self.paramaeters = parameters

        # Should we represent this with it's own getter and make the variable private
        self.finished = False

    @abstractmethod
    def execute(self):
        """
            Executes itself with it's parameters deserialized to a json string
            TODO: Can execution be a template method that just needs to be serialized by subclass implementation
                  BUT each request may not be independent as in just one method call since some might require a connection call prior
        """
        pass

    @abstractmethod
    def get_response(self):
        """
            Retrieves json response and serializes to expected response type
            TODO: When getting a response from the response queue, what do we do when there are events that don't have to do with this command
        """
        pass

    @abstractmethod
    def serialize_request(self):
        """
            Each command will have specific typed parameters that need to be serialized into a json string
            We can use JSON Pickle to serialize and deserialzie from complex to simple parameters. Parameters will have to match tools service type.
        """
        pass

    @abstractmethod
    def deserialize_response(self):
        """ 
            Given a json rpc string response from json rpc client, we have to parse through the methods to deserialize to the appropriate response.
        """
        pass
