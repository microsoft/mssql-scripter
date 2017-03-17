# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from mssql.commands import Command

class Script_Database_Command(Command):
    """
        Script database command that 
    """
    # Not sure if method signature has to match parent 
    def __init__(self, rpc_client, parameters):
        super(Script_Database_Command, self).__init__()

        # Another option is for the caller to create and set the database option.
        self.script_database_options = Script_Database_Options(parameters)

    def execute(self):
        pass

    def get_response(self):
        pass

    def serialize_request(self):
        pass

from future.utils import iteritems
import jsonpickle

class Script_Database_Options(object):
    """
        Holds scripting database options. Used by client.
    """
    def __init__(self, options = None):
    
        # General default scripting options
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

        # TODO: Add the enum options

        if (not options is None):
            current_options = self.__dict__

            for option, value in iteritems(options):
                # Check that the option is valid
                if (not option in current_options):
                    raise ValueError('Invalid option specified')
                
                # TODO: Check for enum allowed values perhaps special case it
                # Option is valid so set it
                current_options[option] = value


    def serialize(self):
        serialized = jsonpickle.encode(self, unpicklable = False)
        return serialized



if __name__ == '__main__':
    my_options = {'ANSIPadding': True, 'AppendToFile': True, 'CheckForObjectExistence': True}

    options = Script_Database_Options(my_options)
    print(options.get_serialize())