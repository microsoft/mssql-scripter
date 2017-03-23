# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
import unittest
#TODO: Clean up this import, perhaps restructure the module
from mssql.commands.scripting_request import *

import subprocess
from subprocess import PIPE
from common.json_rpc_client import Json_Rpc_Client
from common.json_rpc import Json_Rpc_Writer, Json_Rpc_Reader
from io import BytesIO, StringIO

import time
import sys
import json

class Script_Database_Tests(unittest.TestCase):

    def test_basic_script_database_request(self):
        process = subprocess.Popen( [r"D:\repos\sqltoolsservice\src\Microsoft.SqlTools.ServiceLayer\bin\Debug\netcoreapp1.0\win7-x64\Microsoft.SqlTools.ServiceLayer.exe", 
            "--enable-logging"], bufsize=0, stdin=PIPE, stdout=PIPE)

        parameters = {'FilePath': 'D:\\repos\\sql-xplat-cli\\sample_db.sql', 'ConnectionString': 'Server=bro-hb; Database=AdventureWorks2014; User Id=sa; Password=Yukon900', 
        'DatabaseObjects' : None}

        rpc_client = Json_Rpc_Client(process.stdin, process.stdout)
        rpc_client.start()

        request = Scripting_Request(1, rpc_client, parameters)
        request.execute()
        while(not request.completed()):
            response = request.get_response()
            if (not response is None):
                print(response)

        
        process.kill()

    """
        TODO: Test basic script Request
              Test Fail SCript EOFError
              TEst all script scenarios with almost all types of objects scripted
    """

    def test_scripting_response_decoder(self):
        cancel_event = {"jsonrpc": "2.0","method": "scripting/scriptCancel","params": {"operationId": "e18b9538-a7ff-4502-9c33-ac63ed42e5a5"}}
        complete_event = {"jsonrpc": "2.0","method": "scripting/scriptComplete","params": {"operationId": "e18b9538-a7ff-4502-9c33-ac63ed42e5a5"}}
        error_event = {"jsonrpc": "2.0","method": "scripting/scriptError","params": {"operationId": "e18b9538-a7ff-4502-9c33-ac63ed42e5a5"
        , "message": "Scripting error occured", "diagnosticMessage": "error occured during scripting"}}
        
        progress_notification = {"jsonrpc": "2.0","method": "scripting/scriptProgressNotification","params": {"operationId": "e18b9538-a7ff-4502-9c33-ac63ed42e5a5"
        , "status": "Completed", "count": 3, "totalCount" : 12, "scriptingObject" : {"type" : "FullTextCatalog", "schema" : "null", "name" : "SampleFullTextCatalog"}}}

        plan_notification = {"jsonrpc": "2.0","method": "scripting/scriptPlanNotification","params": {"operationId": "e18b9538-a7ff-4502-9c33-ac63ed42e5a5"\
        , "databaseObjects" :[{
            "type": "Database",
            "schema": "null",
            "name": "AdventureWorks2014"
          }], "count" : 10}}

        decoder = Scripting_Response_Decoder()

        cancel_decoded = decoder.decode_response(cancel_event)
        complete_decoded = decoder.decode_response(complete_event)
        error_decoded = decoder.decode_response(error_event)
        progress_notification_decoded = decoder.decode_response(progress_notification)
        plan_notification_decoded = decoder.decode_response(plan_notification)

        self.assertTrue(isinstance(cancel_decoded, ScriptCancelEvent))
        self.assertTrue(isinstance(complete_decoded, ScriptCompleteEvent))
        self.assertTrue(isinstance(error_decoded, ScriptErrorEvent))
        self.assertTrue(isinstance(progress_notification_decoded, ScriptProgressNotificationEvent))
        self.assertTrue(isinstance(plan_notification_decoded, ScriptPlanNotificationEvent))

    def test_default_script_options(self):
        """
            Verifies that default options are created.
        """
        scripting_options = Scripting_Options()
        expected = {'ANSIPadding': False, 'AppendToFile': False, 'CheckForObjectExistence': False, 'ContinueScriptingOnError': False, 'ConvertUDDTsToBaseTypes': False, 
                    'GenerateScriptForDependentObjects': False, 'IncludeDescriptiveHeaders': False, 'IncludeSystemConstraintNames': False, 'IncludeUnsupportedStatements': False, 
                    'SchemaQualifyObjectNames': False, 'ScriptBindings': False, 'SciptionCollations': False, 'ScriptDefaults': False, 'ScriptExtendedProperties': False, 
                    'ScriptLogins': False, 'ScriptObjectLevelPermissions': False, 'ScriptOwner': False, 'ScriptUseDatabase': False, 'ScriptChangeTracking': False, 
                    'ScriptCheckConstraints': False, 'ScriptDataCompressionOptions': False, 'ScriptForeignKey': False, 'ScriptFullTextIndexrs': False, 'ScriptIndexes': False, 
                    'ScriptPrimaryKeys': False, 'ScriptTriggers': False, 'ScriptUniqueKeys': False, 'TypeOfDataToScript': 'SchemaOnly', 'ScriptDropAndCreate': 'ScriptCreate', 
                    'ScriptForTheDatabaseEngineType': 'SingleInstance', 'ScriptStatistics': 'ScriptStatsNone', 'ScriptForServerVersion': 'SQL Server vNext CTP 1.0', 
                    'ScriptForTheDatabaseEngineEdition': 'Microsoft SQL Server Standard Edition'}

        self.assertEqual(scripting_options.get_options(), expected)

    def test_nondefault_script_options(self):
        """
            Verifies only optoins are updated.
        """
        new_options = {'ANSIPadding': True, 'AppendToFile': True, 'TypeOfDataToScript': 'SchemaOnly', 'ScriptDropAndCreate': 'ScriptCreate', 
                    'ScriptForTheDatabaseEngineType': 'SingleInstance', 'ScriptStatistics': 'ScriptStatsNone', 'ScriptForServerVersion': 'SQL Server vNext CTP 1.0', 
                    'ScriptForTheDatabaseEngineEdition': 'Microsoft SQL Server Standard Edition'}
        scripting_options = Scripting_Options(new_options)

        expected = {'ANSIPadding': True, 'AppendToFile': True, 'CheckForObjectExistence': False, 'ContinueScriptingOnError': False, 'ConvertUDDTsToBaseTypes': False, 
                    'GenerateScriptForDependentObjects': False, 'IncludeDescriptiveHeaders': False, 'IncludeSystemConstraintNames': False, 'IncludeUnsupportedStatements': False, 
                    'SchemaQualifyObjectNames': False, 'ScriptBindings': False, 'SciptionCollations': False, 'ScriptDefaults': False, 'ScriptExtendedProperties': False, 
                    'ScriptLogins': False, 'ScriptObjectLevelPermissions': False, 'ScriptOwner': False, 'ScriptUseDatabase': False, 'ScriptChangeTracking': False, 
                    'ScriptCheckConstraints': False, 'ScriptDataCompressionOptions': False, 'ScriptForeignKey': False, 'ScriptFullTextIndexrs': False, 'ScriptIndexes': False, 
                    'ScriptPrimaryKeys': False, 'ScriptTriggers': False, 'ScriptUniqueKeys': False, 'TypeOfDataToScript': 'SchemaOnly', 'ScriptDropAndCreate': 'ScriptCreate', 
                    'ScriptForTheDatabaseEngineType': 'SingleInstance', 'ScriptStatistics': 'ScriptStatsNone', 'ScriptForServerVersion': 'SQL Server vNext CTP 1.0', 
                    'ScriptForTheDatabaseEngineEdition': 'Microsoft SQL Server Standard Edition'}

        self.assertEqual(scripting_options.get_options(), expected)

    def test_invalid_script_options(self):
        """
            Verifies invalid script options throw expected error.
        """
        invalid_options = {'ANSIPadding': 'NonValid', 'AppendToFile': 'Random'}
        
        invalid_server_version = {'ScriptForServerVersion': 'SQL Server 1689'}

        try:
            scripting_options = Scripting_Options(invalid_options)
        except ValueError as exception:
            self.assertEqual(exception.args, ('Option: ANSIPadding has unexpected value type" NonValid',))
        
        try:
            scripting_options = Scripting_Options(invalid_server_version)
        except ValueError as exception:
            self.assertEqual(exception.args, ('Option: ScriptForServerVersion has invalid value: SQL Server 1689',))

    def test_script_database_params_format(self):
        """
            TODO: Update the top level parameters once sql tools service work is finalized.
        """
        params = {'FilePath': 'C:\temp\sample_db.sql' , 'ConnectionString': 'Sample_connection_string' , 'DatabaseObjects': ['Person.Person'] }
        scripting_params = Scripting_Params(params)

        formatted_params = scripting_params.format()
        expected_script_options = {'ANSIPadding': False, 'AppendToFile': False, 'CheckForObjectExistence': False, 'ContinueScriptingOnError': False, 
            'ConvertUDDTsToBaseTypes': False, 'GenerateScriptForDependentObjects': False, 'IncludeDescriptiveHeaders': False, 'IncludeSystemConstraintNames': False, 
            'IncludeUnsupportedStatements': False, 'SchemaQualifyObjectNames': False, 'ScriptBindings': False, 'SciptionCollations': False, 'ScriptDefaults': False, 
            'ScriptExtendedProperties': False, 'ScriptLogins': False, 'ScriptObjectLevelPermissions': False, 'ScriptOwner': False, 'ScriptUseDatabase': False, 
            'ScriptChangeTracking': False, 'ScriptCheckConstraints': False, 'ScriptDataCompressionOptions': False, 'ScriptForeignKey': False, 'ScriptFullTextIndexrs': False, 
            'ScriptIndexes': False, 'ScriptPrimaryKeys': False, 'ScriptTriggers': False, 'ScriptUniqueKeys': False, 'TypeOfDataToScript': 'SchemaOnly', 
            'ScriptDropAndCreate': 'ScriptCreate', 'ScriptForTheDatabaseEngineType': 'SingleInstance', 'ScriptStatistics': 'ScriptStatsNone', 
            'ScriptForServerVersion': 'SQL Server vNext CTP 1.0', 'ScriptForTheDatabaseEngineEdition': 'Microsoft SQL Server Standard Edition'}

        self.assertEqual(formatted_params['FilePath'], 'C:\temp\sample_db.sql')
        self.assertEqual(formatted_params['ConnectionString'], 'Sample_connection_string')
        self.assertEqual(formatted_params['DatabaseObjects'], ['Person.Person'])
        self.assertEqual(formatted_params['ScriptOptions'], expected_script_options)
        
    # Test decoder works on expected responses
    #def test_script_database_response_decoder(self):
    #    decoder = Scripting_Response_Decoder()
    #    response = '{"method": "test/testmethod"}'
    #    json.loads(response, cls=Scripting_Response_Decoder)
    #    print(response)

    # Test submit simple request
    def test_script_database_request(self):
        pass
        # Create the streams
       # input_stream = BytesIO()
       # output_stream = StringIO('{"jsonrpc": "2.0","method": "scripting/scriptProgressNotification","params": {"message": "Responding"}}')
#
       # # Create and start rpc client
       # json_rpc_client = Json_Rpc_Client(input_stream, output_stream)
       # json_rpc_client.start()
#
       # # Form the scripting request
       # params = {'FilePath': 'C:\temp\sample_db.sql' , 'ConnectionString': 'Sample_connection_string' , 'Tables': ['Person.Person'] }
       # request = Scripting_Request(1, json_rpc_client, params)
       # 
       # request.execute()
       # while(not request.finished()):
       #     response = request.get_response()
       #     print(response)


    # Test read response
    # Test state is updated

if __name__ == '__main__':
    unittest.main(warnings='ignore')