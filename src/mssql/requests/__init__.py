# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
import abc

ABC = abc.ABCMeta('ABC', (object,), {})  # compatibile with Python 2 *and* 3


class Request(ABC):
    """
        Abstract command class that all service commands need to subclass.
        Each commands responsibilities:
             Method name in the sql tools service.
             Define it's types necessary for requests and responses.
             Serialization of request parameters.
             Deserialization of responses.

    """
    @abc.abstractmethod
    def execute(self):
        """
            Executes the request
        """
        pass

    @abc.abstractmethod
    def get_response(self):
        """
            Retrieves json response and serializes to expected response type
        """
        pass

    @abc.abstractmethod
    def completed(self):
        """
            returns on the state of the command if it has finished.
        """
        pass
