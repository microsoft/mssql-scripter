# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from mssql.commands import Request
from future.utils import iteritems
from json import JSONDecoder
import json


class Scripting_Request(Request):
    """
        Script database command.
    """
    METHOD_NAME ='scripting/script'

    def __init__(self, id, json_rpc_client, parameters):
        """
            Initializes a command with the json rpc client and necessary parameters.
        """
        assert id != 0
        self.id = id
        self.json_rpc_client = json_rpc_client
        self.params = Scripting_Params(parameters)
        self.finished = False
        self.decoder = Scripting_Response_Decoder()
    def execute(self):
        """
            Submits script db request via json rpc client with formatted parameters and id.
        """
        self.json_rpc_client.submit_request(self.METHOD_NAME, self.params.format(), self.id)
        
    def get_response(self):
        """
            Retrieves the events or response associated with this request and decodes to the explicit type.

            Get the latest event/response from the queue.
        """
        # Check if there are any immediate response to the request
        response = self.json_rpc_client.get_response(self.id)
        if (not response is None):
            return self.decoder.decode_response(response)
        
        # No response, check for events
        event = self.json_rpc_client.get_response()
        if (not event is None):
            event_type = self.decoder.decode_response(event)
            # Request is completed
            if (isinstance(event_type, ScriptCompleteEvent)):
                self.finished = True
            
            return event_type
        
        return None

    def dispose(self):
        # Remove response queue from json rpc client
        json_rpc_client.request_finished(self.id)

    def completed(self):
        return self.finished

class ScriptCancelEvent(object):
    def __init__(self, params):
        self.operation_id = params["operationId"]

class ScriptCompleteEvent(object):
    def __init__(self, params):
        self.operation_id = params["operationId"]

class ScriptErrorEvent(object):
    def __init__(self, params):
        self.operation_id = params["operationId"]
        self.message = params["message"]
        self.diagnostic_message = params["diagnosticMessage"]

class ScriptPlanNotificationEvent(object):
    def __init__(self, params):
        self.operation_id = params["operationId"]
        # TODO: We can separate out the actual object 
        self.database_objects = params["databaseObjects"]
        self.count = params["count"]

class ScriptProgressNotificationEvent(object):
    def __init__(self, params):
        self.operation_id = params["operationId"]
        self.scripting_object = params["scriptingObject"]
        self.status = params["status"]
        self.count = params["count"]
        self.total_count = params["totalCount"]

class ScriptResponse(object):
    def __init__(self, params):
        self.operation_id = params["operationId"]

class Scripting_Response_Decoder(object):
    """
        Responsibile for decoding json response into it's appropriate  type.
    """
    def __init__(self):
        # response map 
        self.response_dispatcher = {'scripting/scriptCancel' : ScriptCancelEvent,
                                    'scripting/scriptComplete': ScriptCompleteEvent,
                                    'scripting/scriptError': ScriptErrorEvent,
                                    'scripting/scriptPlanNotification': ScriptPlanNotificationEvent,
                                    'scripting/scriptProgressNotification': ScriptProgressNotificationEvent,
                                    'id': ScriptResponse }

    def decode_response(self, obj):
        """
            Based on the method name, we return the appropriate event object.
        """
        if ("method" in obj):
            response_name = obj["method"]
            if (response_name in self.response_dispatcher):
                return self.response_dispatcher[response_name](obj["params"])
        
        if ("id" in obj and "result" in obj):
            print("Found Response")
            return self.response_dispatcher["id"](obj["result"])

        #TODO: Log error 
        # Return the json string normally
        return obj

class Scripting_Params(object):
    """
        Holds scripting database options. Used by client.
    """
    def __init__(self, parameters):
        self.file_path = parameters['FilePath']
        self.connection_string = parameters['ConnectionString']
        self.database_objects = parameters['DatabaseObjects']
        self.scripting_options = Scripting_Options(parameters)  

    def format(self):
        """
            Returns a dictionary of script database parameters nested with it's sql tools service equivalent class name.
        """
        return {'FilePath' : self.file_path,
                'ConnectionString' : self.connection_string,
                'DatabaseObjects' : self.database_objects,
                'ScriptOptions' : self.scripting_options.get_options()}

class Scripting_Options(object):
    """
        Holds various scripting options that are available in the script database wizard in SSMS.
    """
    scripting_option_map = {        
        'TypeOfDataToScript' : ['SchemaAndData', 'DataOnly', 'SchemaOnly'],
        'ScriptDropAndCreate' : ['ScriptCreate', 'ScriptDrop', 'ScriptCreateDrop'],
        'ScriptForTheDatabaseEngineType' : ['SingleInstance', 'SqlAzure'],
        'ScriptStatistics' : ['ScriptStatsAll', 'ScriptStatsNone', 'ScriptStatsDll'],
        'ScriptForServerVersion' : ['SQL Server 2005', 'SQL Server 2008', 'SQL Server 2008 R2', 
                                    'SQL Server 2012', 'SQL Server 2014', 'SQL Server 2016',
                                    'SQL Server vNext CTP 1.0'],
        'ScriptForTheDatabaseEngineEdition' : ['Microsoft SQL Server Standard Edition', 'Microsoft SQL Server Personal Edition'
                                               'Microsoft SQL Server Express Edition', 'Microsoft SQL Server Enterprise Edition',
                                               'Microsoft SQL Server Stretch Database Edition'] }

    def __init__(self, parameters = None):
        """
            Initializes database options with default values. If parameters were passed in, script options will only update valid ones.
        """
        # General Default scripting options
        self.ANSIPadding = False
        self.AppendToFile = False
        self.CheckForObjectExistence = False
        self.ContinueScriptingOnError = False
        self.ConvertUDDTsToBaseTypes = False
        self.GenerateScriptForDependentObjects = False
        self.IncludeDescriptiveHeaders = False
        self.IncludeSystemConstraintNames = False
        self.IncludeUnsupportedStatements = False
        self.SchemaQualifyObjectNames = False
        self.ScriptBindings = False
        self.SciptionCollations = False
        self.ScriptDefaults = False
        self.ScriptExtendedProperties = False
        self.ScriptLogins = False
        self.ScriptObjectLevelPermissions = False
        self.ScriptOwner = False
        self.ScriptUseDatabase = False

        # Default Table/View options
        self.ScriptChangeTracking = False
        self.ScriptCheckConstraints = False
        self.ScriptDataCompressionOptions = False
        self.ScriptForeignKey = False
        self.ScriptFullTextIndexrs = False
        self.ScriptIndexes = False
        self.ScriptPrimaryKeys = False
        self.ScriptTriggers = False
        self.ScriptUniqueKeys = False

        # Scripting options that are limited
        self.TypeOfDataToScript = 'SchemaOnly'
        self.ScriptDropAndCreate = 'ScriptCreate'
        self.ScriptForTheDatabaseEngineType = 'SingleInstance'
        self.ScriptStatistics = 'ScriptStatsNone'
        self.ScriptForServerVersion = 'SQL Server vNext CTP 1.0'
        self.ScriptForTheDatabaseEngineEdition = 'Microsoft SQL Server Standard Edition'

        if (not parameters is None):
            self.update_options(parameters)

    def update_options(self, parameters):
        """
            Updates options from passed in parameters only if they are valid.
        """
        default_options = vars(self)
        for option, value in iteritems(parameters):         
            if (option in default_options):
                if (option in self.scripting_option_map):
                    if (not value in self.scripting_option_map[option]):
                        raise ValueError('Option: {0} has invalid value: {1}'.format(option, value))
                elif (not isinstance(value, bool)):
                    raise ValueError('Option: {0} has unexpected value type" {1}'.format(option, value))
                # set the value if we pass all the checks
                default_options[option] = value

    def get_options(self):
        """
            Returns a dictionary of all options
        """
        return vars(self)

