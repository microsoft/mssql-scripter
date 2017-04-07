# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from mssql.contracts import Request
from future.utils import iteritems

import logging

logger = logging.getLogger('mssql-scripter.contracts.scripting')


class Scripting_Request(Request):
    """
        SqlTools Service scripting service scripting request.
    """
    METHOD_NAME = u'scripting/script'

    def __init__(self, id, json_rpc_client, parameters):
        """
            Create a scripting request command.
        """
        assert id != 0
        self.id = id
        self.finished = False
        self.json_rpc_client = json_rpc_client
        self.params = Scripting_Params(parameters)
        self.decoder = Scripting_Response_Decoder()

    def execute(self):
        """
            submit scripting request to sql tools service.
        """
        logger.info(
            u'Submitting scripting request id: {} with targetfile: {}'.format(
                self.id, self.params.file_path))

        self.json_rpc_client.submit_request(
            self.METHOD_NAME, self.params.format(), self.id)

    def get_response(self):
        """
            Get response for this request or global event.
        """
        # Check if there are any immediate response to the request.
        response = self.json_rpc_client.get_response(self.id)
        decoded_response = None

        if response:
            decoded_response = self.decoder.decode_response(response)
            logger.debug(
                u'Scripting request received response: {}'.format(decoded_response))
        # No response, check for events.
        event = self.json_rpc_client.get_response()
        if event:
            decoded_response = self.decoder.decode_response(event)
            logger.debug(
                u'Scripting request received response: {}'.format(decoded_response))
            # Request is completed.
            if (isinstance(decoded_response, ScriptCompleteEvent)
                    or isinstance(decoded_response, ScriptErrorEvent)):
                self.finished = True
                self.json_rpc_client.request_finished(self.id)

        return decoded_response

    def completed(self):
        """
            Get current request state.
        """
        return self.finished


class Scripting_Params(object):
    """
        Scripting request parameters.
    """

    def __init__(self, parameters):
        self.file_path = parameters[u'FilePath']
        self.connection_string = parameters[u'ConnectionString']
        # TODO: Renable when this option is supported.
        #self.scripting_objects = parameters['scriptingObjects']
        self.scripting_options = Scripting_Options(parameters)

    def format(self):
        """
            Format paramaters into a dictionary.
        """
        return {u'FilePath': self.file_path,
                u'ConnectionString': self.connection_string,
                # TODO: Renable when support is added
                #'DatabaseObjects' : self.database_objects,
                u'ScriptOptions': self.scripting_options.get_options()}


class Scripting_Options(object):
    """
        Advanced scripting options.
    """
    scripting_option_map = {
        u'TypeOfDataToScript': [
            u'SchemaAndData',
            u'DataOnly',
            u'SchemaOnly'],
        u'ScriptDropAndCreate': [
            u'ScriptCreate',
            u'ScriptDrop',
            u'ScriptCreateDrop'],
        u'ScriptForTheDatabaseEngineType': [
            u'SingleInstance',
            u'SqlAzure'],
        u'ScriptStatistics': [
            u'ScriptStatsAll',
            u'ScriptStatsNone',
            u'ScriptStatsDll'],
        u'ScriptForServerVersion': [
            u'SQL Server 2005',
            u'SQL Server 2008',
            u'SQL Server 2008 R2',
            u'SQL Server 2012',
            u'SQL Server 2014',
            u'SQL Server 2016',
            u'SQL Server vNext CTP 1.0'],
        u'ScriptForTheDatabaseEngineEdition': [
            u'Microsoft SQL Server Standard Edition',
            u'Microsoft SQL Server Personal Edition'
            u'Microsoft SQL Server Express Edition',
            u'Microsoft SQL Server Enterprise Edition',
            u'Microsoft SQL Server Stretch Database Edition',
            u'Microsoft Azure SQL Database Edition',
            u'Microsoft Azure Data Warehouse Edition', ]}

    def __init__(self, parameters=None):
        """
            Create default or non default scripting options based on parameters.
        """
        # General Default scripting options.
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

        # Default Table/View options.
        self.ScriptChangeTracking = False
        self.ScriptCheckConstraints = False
        self.ScriptDataCompressionOptions = False
        self.ScriptForeignKey = False
        self.ScriptFullTextIndexrs = False
        self.ScriptIndexes = False
        self.ScriptPrimaryKeys = False
        self.ScriptTriggers = False
        self.ScriptUniqueKeys = False

        # Scripting options that are limited.
        self.TypeOfDataToScript = u'SchemaOnly'
        self.ScriptDropAndCreate = u'ScriptCreate'
        self.ScriptForTheDatabaseEngineType = u'SingleInstance'
        self.ScriptStatistics = u'ScriptStatsNone'
        self.ScriptForServerVersion = u'SQL Server vNext CTP 1.0'
        self.ScriptForTheDatabaseEngineEdition = u'Microsoft SQL Server Standard Edition'

        if parameters:
            self.update_options(parameters)

    def update_options(self, parameters):
        """
            Update default options to passed in options.
        """
        default_options = vars(self)
        for option, value in iteritems(parameters):
            if option in default_options:
                if option in self.scripting_option_map:
                    if value not in self.scripting_option_map[option]:
                        raise ValueError(
                            u'Option: {} has invalid value: {}'.format(
                                option, value))
                elif not isinstance(value, bool):
                    raise ValueError(
                        u'Option: {} has unexpected value type" {}'.format(
                            option, value))
                # set the value if we pass all the checks.
                default_options[option] = value

    def get_options(self):
        """
            Return a dictionary of all options
        """
        return vars(self)

#
#   Various Scripting Events.
#


class ScriptCancelEvent(object):
    def __init__(self, params):
        self.operation_id = params[u'operationId']


class ScriptCompleteEvent(object):
    def __init__(self, params):
        self.operation_id = params[u'operationId']


class ScriptErrorEvent(object):
    def __init__(self, params):
        self.operation_id = params[u'operationId']
        self.message = params[u'message']
        self.diagnostic_message = params[u'diagnosticMessage']


class ScriptPlanNotificationEvent(object):
    def __init__(self, params):
        self.operation_id = params[u'operationId']
        # TODO: We can separate out the actual objects or return a list of the
        # objects to the client.
        self.database_objects = params[u'databaseObjects']
        self.count = params[u'count']


class ScriptProgressNotificationEvent(object):
    def __init__(self, params):
        self.operation_id = params[u'operationId']
        self.scripting_object = params[u'scriptingObject']
        self.status = params[u'status']
        self.count = params[u'count']
        self.total_count = params[u'totalCount']


class ScriptResponse(object):
    def __init__(self, params):
        self.operation_id = params[u'operationId']


class Scripting_Response_Decoder(object):
    """
        Decode response dictionary into scripting parameter type.
    """

    def __init__(self):
        # response map.
        self.response_dispatcher = {
            u'scripting/scriptCancel': ScriptCancelEvent,
            u'scripting/scriptComplete': ScriptCompleteEvent,
            u'scripting/scriptError': ScriptErrorEvent,
            u'scripting/scriptPlanNotification': ScriptPlanNotificationEvent,
            u'scripting/scriptProgressNotification': ScriptProgressNotificationEvent,
            u'id': ScriptResponse}

    def decode_response(self, obj):
        """
            Decode valid response.
        """
        if u'method' in obj:
            response_name = obj[u'method']
            if response_name in self.response_dispatcher:
                # Handle event received.
                return self.response_dispatcher[response_name](obj[u'params'])

        if u'id' in obj and u'result' in obj:
            # Handle response received.
            return self.response_dispatcher[u'id'](obj[u'result'])

        logger.debug(
            u'Unable to decode response to a event type: {}'.format(obj))
        # Unable to decode, return json string.
        return obj
