# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from future.utils import iteritems
from mssqlscripter.jsonrpc.contracts import Request

import copy
import logging

logger = logging.getLogger(u'mssqlscripter.jsonrpc.contracts.scriptingservice')


class ScriptingRequest(Request):
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
        self.params = ScriptingParams(parameters)
        self.decoder = ScriptingResponseDecoder()

    def execute(self):
        """
            submit scripting request to sql tools service.
        """
        logger.info(
            u'Submitting scripting request id: {} with targetfile: {}'.format(
                self.id, self.params.file_path))

        scrubbed_parameters = copy.deepcopy(self.params)
        scrubbed_parameters.connection_string = '*********'
        logger.debug(scrubbed_parameters.format())
        self.json_rpc_client.submit_request(
            self.METHOD_NAME, self.params.format(), self.id)

    def get_response(self):
        """
            Get latest response, event or exception if it occured.
        """
        try:
            response = self.json_rpc_client.get_response(self.id)
            decoded_response = None

            if response:
                logger.debug(response)
                # Decode response to either response or event type.
                decoded_response = self.decoder.decode_response(response)

                logger.debug(
                    u'Scripting request received response: {}'.format(decoded_response))
                if (isinstance(decoded_response, ScriptCompleteEvent)):
                    self.finished = True
                    self.json_rpc_client.request_finished(self.id)

            return decoded_response

        except Exception as error:
            # Return a scripting error event.
            self.finished = True
            self.json_rpc_client.request_finished(self.id)
            logger.debug('Scripting request received exception: {}'.format(str(error)))
            exception = {
                u'operationId': self.id,
                u'sequenceNumber': None,
                u'success': False,
                u'canceled': False,
                u'hasError': True,
                u'errorMessage': u'Scripting request encountered a exception',
                u'errorDetails': error.args,
            }

            return ScriptCompleteEvent(exception)

    def completed(self):
        """
            Get current request state.
        """
        return self.finished


class ScriptingParams(object):
    """
        Scripting request parameters.
    """

    def __init__(self, parameters):
        self.file_path = parameters[u'FilePath']
        self.connection_string = parameters[u'ConnectionString']
        self.script_destination = parameters[u'ScriptDestination']
        self.scripting_options = ScriptingOptions(parameters)

        # List of scripting objects.
        self.include_objects = ScriptingObjects(
            parameters[u'IncludeObjects'] if u'IncludeObjects' in parameters else None)
        self.exclude_objects = ScriptingObjects(
            parameters[u'ExcludeObjects'] if u'ExcludeObjects' in parameters else None)

    def format(self):
        """
            Format paramaters into a dictionary.
        """
        return {u'FilePath': self.file_path,
                u'ConnectionString': self.connection_string,
                u'IncludeObjectCriteria': self.include_objects.format(),
                u'ExcludeObjectCriteria': self.exclude_objects.format(),
                u'ScriptOptions': self.scripting_options.get_options(),
                u'ScriptDestination': self.script_destination}


class ScriptingObjects(object):
    """
        Represent a database object via it's type, schema, and name.
    """

    def __init__(self, scripting_objects):
        self.list_of_objects = []
        if scripting_objects:
            for item in scripting_objects:
                index = item.find('.')
                if index > 0:
                    schema = item[0:index]
                    name = item[index + 1:]
                else:
                    schema = None
                    name = item
                self.add_scripting_object(schema=schema, name=name)

    def add_scripting_object(self, script_type=None, schema=None, name=None):
        """
            Serialize scripting object into a JSON Scripting object.
        """
        object_dict = {
            u'Type': script_type,
            u'Schema': schema,
            u'Name': name
        }

        self.list_of_objects.append(object_dict)

    def format(self):
        return self.list_of_objects


class ScriptingOptions(object):
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
        u'TargetDatabaseEngineType': [
            u'SingleInstance',
            u'SqlAzure'],
        u'ScriptStatistics': [
            u'ScriptStatsAll',
            u'ScriptStatsNone',
            u'ScriptStatsDll'],
        u'ScriptCompatibilityOption': [
            u'Script90Compat',
            u'Script100Compat',
            u'Script105Compat',
            u'Script110Compat',
            u'Script120Compat',
            u'Script130Compat',
            u'Script140Compat'],
        u'TargetDatabaseEngineEdition': [
            u'SqlServerStandardEdition',
            u'SqlServerPersonalEdition',
            u'SqlServerExpressEdition',
            u'SqlServerEnterpriseEdition',
            u'SqlServerStretchDatabaseEdition'
            u'SqlAzureDatabaseEdition',
            u'SqlDatawarehouseEdition']}

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
        self.TargetDatabaseEngineType = u'SingleInstance'
        self.ScriptStatistics = u'ScriptStatsNone'
        self.ScriptCompatibilityOption = u'Script140Compat'
        self.TargetDatabaseEngineEdition = u'SqlServerStandardEdition'

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


class ScriptCompleteEvent(object):
    def __init__(self, params):
        self.operation_id = params[u'operationId']
        self.sequenceNumber = params[u'sequenceNumber']
        self.error_details = params[u'errorDetails']
        self.error_message = params[u'errorMessage']
        self.has_error = params[u'hasError']
        self.canceled = params[u'canceled']
        self.success = params[u'success']


class ScriptPlanNotificationEvent(object):
    def __init__(self, params):
        self.operation_id = params[u'operationId']
        self.sequenceNumber = params[u'sequenceNumber']
        self.scripting_objects = params[u'scriptingObjects']
        self.count = params[u'count']


class ScriptProgressNotificationEvent(object):
    def __init__(self, params):
        self.operation_id = params[u'operationId']
        self.sequenceNumber = params[u'sequenceNumber']
        self.scripting_object = params[u'scriptingObject']
        self.status = params[u'status']
        self.completed_count = params[u'completedCount']
        self.total_count = params[u'totalCount']


class ScriptResponse(object):
    def __init__(self, params):
        self.operation_id = params[u'operationId']


class ScriptingResponseDecoder(object):
    """
        Decode response dictionary into scripting parameter type.
    """

    def __init__(self):
        # response map.
        self.response_dispatcher = {
            u'scripting/scriptComplete': ScriptCompleteEvent,
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
