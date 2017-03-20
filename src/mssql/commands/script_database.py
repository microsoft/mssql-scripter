# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from mssql.commands import Command
from future.utils import iteritems

class Script_Database_Command(Command):
    """
        Script database command.
    """
    METHOD_NAME ='scripting/ScriptDatabase'

    def __init__(self, id, json_rpc_client, parameters = None):
        self.id = id
        self.json_rpc_client = json_rpc_client
        self.params = Script_Database_Options(parameters)
        self.Finished = False

    def execute(self):
        self.json_rpc_client.submit_request(self.METHOD_NAME, self.params.format())

    def get_response(self):
        # Will need to come back once we change the implementation on the event queue
        response = rpc_client.get_response()
        if (response is None):
            response = rpc_client.get_response(self.id)

        # Convert response to typed event
        # No id = event
        # Responses are either error or result

        return response

    def dispose(self):
        # Remove response queue from json rpc client
        json_rpc_client.request_finished(self.id)

class Script_Database_Params(object):
    """
        Holds scripting database options. Used by client.
    """
    def __init__(self, parameters):
        self.file_path = parameters['targetfile']
        self.connection_string = parameters['connectionstring']
        
        self.script_options = Script_Options(parameters)  

    def format(self):
        return {'test parameter' : self.test_parameter,
                'ScriptOptions' : vars(self.script_options)}

class Script_Options(object):

    def __init__(self, parameters = None):

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

        if (not parameters is None):
            self._update_options(parameters)
           
    def _update_options(self, parameters):
        # Only update valid options
        default_options = vars(self)
        for option, value in iteritems(parameters):         
            if (option in default_options):
                default_options[option] = value

if __name__ == '__main__':
    sample_options = {'ScriptTriggers': True}
    options = Script_Database_Params(sample_options)
    command = Script_Database_Command(None)