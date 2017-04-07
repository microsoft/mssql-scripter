# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
from mssql.contracts.scripting import *

from mssql.common.json_rpc_client import Json_Rpc_Client
from mssql.common.json_rpc import Json_Rpc_Writer, Json_Rpc_Reader
from io import BytesIO

import unittest
import os


class Scripting_Request_Tests(unittest.TestCase):
    """
        Scripting request tests
    """

    def test_succesful_scripting_response_AdventureWorks2014(self):
        """
            Verifies that the scripting response of a successful request is read succesfully with a sample request against AdventureWorks2014.
        """
        with open(self.get_test_baseline('adventureworks2014_baseline.txt'), 'r+b', buffering=0) as response_file:
            request_stream = BytesIO(b'')
            rpc_client = Json_Rpc_Client(request_stream, response_file)
            rpc_client.start()
            # Submit a dummy request
            parameters = {
                'FilePath': 'Sample_File_Path',
                'ConnectionString': 'Sample_connection_string',
                'IncludeObjectCriteria' : None,
                'ExcludeObjectCriteria' : None,
                'DatabaseObjects': None}
            request = Scripting_Request(1, rpc_client, parameters)

            self.verify_response_count(
                request=request,
                response_count=1,
                plan_notification_count=1,
                progress_count=375,
                complete_count=1,
                error_count=0)

            rpc_client.shutdown()

    def test_scripting_response_decoder(self):
        cancel_event = {
            'jsonrpc': '2.0',
            'method': 'scripting/scriptCancel',
            'params': {
                'operationId': 'e18b9538-a7ff-4502-9c33-ac63ed42e5a5'}}
        complete_event = {
            'jsonrpc': '2.0',
            'method': 'scripting/scriptComplete',
            'params': {
                'operationId': 'e18b9538-a7ff-4502-9c33-ac63ed42e5a5'}}
        error_event = {
            'jsonrpc': '2.0',
            'method': 'scripting/scriptError',
            'params': {
                'operationId': 'e18b9538-a7ff-4502-9c33-ac63ed42e5a5',
                'message': 'Scripting error occured',
                'diagnosticMessage': 'error occured during scripting'}}

        progress_notification = {
            'jsonrpc': '2.0',
            'method': 'scripting/scriptProgressNotification',
            'params': {
                'operationId': 'e18b9538-a7ff-4502-9c33-ac63ed42e5a5',
                'status': 'Completed',
                'count': 3,
                'totalCount': 12,
                'scriptingObject': {
                    'type': 'FullTextCatalog',
                    'schema': 'null',
                    'name': 'SampleFullTextCatalog'}}}

        plan_notification = {
            'jsonrpc': '2.0',
            'method': 'scripting/scriptPlanNotification',
            'params': {
                'operationId': 'e18b9538-a7ff-4502-9c33-ac63ed42e5a5',
                'databaseObjects': [
                    {
                        'type': 'Database',
                        'schema': 'null',
                        'name': 'AdventureWorks2014'}],
                'count': 10}}

        decoder = Scripting_Response_Decoder()

        cancel_decoded = decoder.decode_response(cancel_event)
        complete_decoded = decoder.decode_response(complete_event)
        error_decoded = decoder.decode_response(error_event)
        progress_notification_decoded = decoder.decode_response(
            progress_notification)
        plan_notification_decoded = decoder.decode_response(plan_notification)

        self.assertTrue(isinstance(cancel_decoded, ScriptCancelEvent))
        self.assertTrue(isinstance(complete_decoded, ScriptCompleteEvent))
        self.assertTrue(isinstance(error_decoded, ScriptErrorEvent))
        self.assertTrue(
            isinstance(
                progress_notification_decoded,
                ScriptProgressNotificationEvent))
        self.assertTrue(
            isinstance(
                plan_notification_decoded,
                ScriptPlanNotificationEvent))

    def test_scripting_response_decoder_invalid(self):
        """
            Verifies that the decoder could not decode to a scripting event type.
        """
        cancel_event = {
            'jsonrpc': '2.0',
            'method': 'query/queryCancelled',
            'params': {
                'operationId': 'e18b9538-a7ff-4502-9c33-ac63ed42e5a5'}}
        complete_event = {
            'jsonrpc': '2.0',
            'method': 'connect/connectionComplete',
            'params': {
                'operationId': 'e18b9538-a7ff-4502-9c33-ac63ed42e5a5'}}

        decoder = Scripting_Response_Decoder()

        cancel_decoded = decoder.decode_response(cancel_event)
        complete_decoded = decoder.decode_response(complete_event)

        # both events should remain untouched.
        self.assertTrue(isinstance(cancel_decoded, dict))
        self.assertTrue(isinstance(complete_decoded, dict))

    def test_default_script_options(self):
        """
            Verifies that default options are created.
        """
        scripting_options = Scripting_Options()
        expected = {
            'ANSIPadding': False,
            'AppendToFile': False,
            'CheckForObjectExistence': False,
            'ContinueScriptingOnError': False,
            'ConvertUDDTsToBaseTypes': False,
            'GenerateScriptForDependentObjects': False,
            'IncludeDescriptiveHeaders': False,
            'IncludeSystemConstraintNames': False,
            'IncludeUnsupportedStatements': False,
            'SchemaQualifyObjectNames': False,
            'ScriptBindings': False,
            'SciptionCollations': False,
            'ScriptDefaults': False,
            'ScriptExtendedProperties': False,
            'ScriptLogins': False,
            'ScriptObjectLevelPermissions': False,
            'ScriptOwner': False,
            'ScriptUseDatabase': False,
            'ScriptChangeTracking': False,
            'ScriptCheckConstraints': False,
            'ScriptDataCompressionOptions': False,
            'ScriptForeignKey': False,
            'ScriptFullTextIndexrs': False,
            'ScriptIndexes': False,
            'ScriptPrimaryKeys': False,
            'ScriptTriggers': False,
            'ScriptUniqueKeys': False,
            'TypeOfDataToScript': 'SchemaOnly',
            'ScriptDropAndCreate': 'ScriptCreate',
            'ScriptForTheDatabaseEngineType': 'SingleInstance',
            'ScriptStatistics': 'ScriptStatsNone',
            'ScriptForServerVersion': 'SQL Server vNext CTP 1.0',
            'ScriptForTheDatabaseEngineEdition': 'Microsoft SQL Server Standard Edition'}

        self.assertEqual(scripting_options.get_options(), expected)

    def test_nondefault_script_options(self):
        """
            Verifies only valid options are updated.
        """
        new_options = {
            'ANSIPadding': True,
            'AppendToFile': True,
            'TypeOfDataToScript': 'SchemaOnly',
            'ScriptDropAndCreate': 'ScriptCreate',
            'ScriptForTheDatabaseEngineType': 'SingleInstance',
            'ScriptStatistics': 'ScriptStatsNone',
            'ScriptForServerVersion': 'SQL Server vNext CTP 1.0',
            'ScriptForTheDatabaseEngineEdition': 'Microsoft SQL Server Standard Edition'}
        scripting_options = Scripting_Options(new_options)

        expected = {
            'ANSIPadding': True,
            'AppendToFile': True,
            'CheckForObjectExistence': False,
            'ContinueScriptingOnError': False,
            'ConvertUDDTsToBaseTypes': False,
            'GenerateScriptForDependentObjects': False,
            'IncludeDescriptiveHeaders': False,
            'IncludeSystemConstraintNames': False,
            'IncludeUnsupportedStatements': False,
            'SchemaQualifyObjectNames': False,
            'ScriptBindings': False,
            'SciptionCollations': False,
            'ScriptDefaults': False,
            'ScriptExtendedProperties': False,
            'ScriptLogins': False,
            'ScriptObjectLevelPermissions': False,
            'ScriptOwner': False,
            'ScriptUseDatabase': False,
            'ScriptChangeTracking': False,
            'ScriptCheckConstraints': False,
            'ScriptDataCompressionOptions': False,
            'ScriptForeignKey': False,
            'ScriptFullTextIndexrs': False,
            'ScriptIndexes': False,
            'ScriptPrimaryKeys': False,
            'ScriptTriggers': False,
            'ScriptUniqueKeys': False,
            'TypeOfDataToScript': 'SchemaOnly',
            'ScriptDropAndCreate': 'ScriptCreate',
            'ScriptForTheDatabaseEngineType': 'SingleInstance',
            'ScriptStatistics': 'ScriptStatsNone',
            'ScriptForServerVersion': 'SQL Server vNext CTP 1.0',
            'ScriptForTheDatabaseEngineEdition': 'Microsoft SQL Server Standard Edition'}

        self.assertEqual(scripting_options.get_options(), expected)

    def test_invalid_script_options(self):
        """
            Verifies invalid script options throw expected error.
        """
        invalid_options = {'ANSIPadding': 'NonValid'}

        invalid_server_version = {'ScriptForServerVersion': 'SQL Server 1689'}

        try:
            scripting_options = Scripting_Options(invalid_options)
        except ValueError as exception:
            self.assertEqual(
                exception.args, ('Option: ANSIPadding has unexpected value type" NonValid',))

        try:
            scripting_options = Scripting_Options(invalid_server_version)
        except ValueError as exception:
            self.assertEqual(
                exception.args,
                ('Option: ScriptForServerVersion has invalid value: SQL Server 1689',
                 ))

    def test_script_database_params_format(self):
        """
            Verifies the database parameters are formatted properly.
        """
        params = {
            'FilePath': 'C:\temp\sample_db.sql',
            'ConnectionString': 'Sample_connection_string',
            'IncludeObjectCriteria' : [],
            'ExcludeObjectCriteria' : [],
            'DatabaseObjects': ['Person.Person']}
        scripting_params = Scripting_Params(params)

        formatted_params = scripting_params.format()
        expected_script_options = {
            'ANSIPadding': False,
            'AppendToFile': False,
            'CheckForObjectExistence': False,
            'ContinueScriptingOnError': False,
            'ConvertUDDTsToBaseTypes': False,
            'GenerateScriptForDependentObjects': False,
            'IncludeDescriptiveHeaders': False,
            'IncludeSystemConstraintNames': False,
            'IncludeUnsupportedStatements': False,
            'SchemaQualifyObjectNames': False,
            'ScriptBindings': False,
            'SciptionCollations': False,
            'ScriptDefaults': False,
            'ScriptExtendedProperties': False,
            'ScriptLogins': False,
            'ScriptObjectLevelPermissions': False,
            'ScriptOwner': False,
            'ScriptUseDatabase': False,
            'ScriptChangeTracking': False,
            'ScriptCheckConstraints': False,
            'ScriptDataCompressionOptions': False,
            'ScriptForeignKey': False,
            'ScriptFullTextIndexrs': False,
            'ScriptIndexes': False,
            'ScriptPrimaryKeys': False,
            'ScriptTriggers': False,
            'ScriptUniqueKeys': False,
            'TypeOfDataToScript': 'SchemaOnly',
            'ScriptDropAndCreate': 'ScriptCreate',
            'ScriptForTheDatabaseEngineType': 'SingleInstance',
            'ScriptStatistics': 'ScriptStatsNone',
            'ScriptForServerVersion': 'SQL Server vNext CTP 1.0',
            'ScriptForTheDatabaseEngineEdition': 'Microsoft SQL Server Standard Edition'}

        self.assertEqual(formatted_params['FilePath'], 'C:\temp\sample_db.sql')
        self.assertEqual(
            formatted_params['ConnectionString'],
            'Sample_connection_string')
        # Reenable assertion below when the option is supported
        #self.assertEqual(formatted_params['DatabaseObjects'], ['Person.Person'])
        self.assertEqual(
            formatted_params['ScriptOptions'],
            expected_script_options)

    def verify_response_count(
            self,
            request,
            response_count,
            plan_notification_count,
            progress_count,
            complete_count,
            error_count,
            func=None):
        """
            Helper to verify expected response count from a request
        """
        progress_notification_event = 0
        complete_event = 0
        response_event = 0
        plan_notification_event = 0
        error_event = 0
        request.execute()

        while(not request.completed()):
            response = request.get_response()
            if (func is not None):
                func(self, response)
            if (isinstance(response, ScriptProgressNotificationEvent)):
                progress_notification_event += 1
            elif (isinstance(response, ScriptCompleteEvent)):
                complete_event += 1
            elif (isinstance(response, ScriptResponse)):
                response_event += 1
            elif (isinstance(response, ScriptPlanNotificationEvent)):
                plan_notification_event += 1
            elif (isinstance(response, ScriptErrorEvent)):
                error_event += 1
        # TODO: Renable this check once we give the process time to process request.
        #self.assertEqual(response_event, response_count)
        self.assertEqual(plan_notification_event, plan_notification_count)
        self.assertEqual(progress_notification_event, progress_count)
        self.assertEqual(complete_event, complete_count)
        self.assertEqual(error_event, error_count)

    def get_test_baseline(self, file_name):
        """
            Helper method to get baseline file.
        """
        return os.path.abspath(
            os.path.join(
                os.path.abspath(__file__),
                '..',
                'scripting_baselines',
                file_name))


if __name__ == '__main__':
    unittest.main()
