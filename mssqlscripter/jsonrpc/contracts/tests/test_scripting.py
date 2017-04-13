# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import io
import os
import unittest

import mssqlscripter.jsonrpc.jsonrpcclient as json_rpc_client
import mssqlscripter.jsonrpc.contracts.scripting as scripting

class ScriptingRequestTests(unittest.TestCase):

    """
        Scripting request tests.
    """

    def test_succesful_scripting_response_AdventureWorks2014(self):
        """
            Verifies that the scripting response of a successful request is read succesfully with a sample request against AdventureWorks2014.
        """
        with open(self.get_test_baseline(u'adventureworks2014_baseline.txt'), u'r+b', buffering=0) as response_file:
            request_stream = io.BytesIO(b'')
            rpc_client = json_rpc_client.JsonRpcClient(
                request_stream, response_file)
            rpc_client.start()
            # Submit a dummy request.
            parameters = {
                u'FilePath': u'Sample_File_Path',
                u'ConnectionString': u'Sample_connection_string',
                u'IncludeObjectCriteria': None,
                u'ExcludeObjectCriteria': None,
                u'DatabaseObjects': None}
            request = scripting.ScriptingRequest(1, rpc_client, parameters)

            self.verify_response_count(
                request=request,
                response_count=1,
                plan_notification_count=1,
                progress_count=375,
                complete_count=1,
                error_count=0)

            rpc_client.shutdown()

    def test_scripting_criteria_parameters(self):
        """
            Verify scripting objects are properly parsed.
        """
        include_objects = [u'schema1.table1', u'table2']
        include_criteria = scripting.ScriptingObjects(include_objects)
        include_formatted = include_criteria.format()

        scripting_object_1 = include_formatted[0]
        scripting_object_2 = include_formatted[1]

        self.assertEqual(scripting_object_1[u'Schema'], u'schema1')
        self.assertEqual(scripting_object_1[u'Name'], u'table1')
        self.assertEqual(scripting_object_1[u'Type'], None)

        self.assertEqual(scripting_object_2[u'Schema'], None)
        self.assertEqual(scripting_object_2[u'Name'], u'table2')
        self.assertEqual(scripting_object_2[u'Type'], None)

    def test_scripting_response_decoder(self):
        cancel_event = {
            u'jsonrpc': u'2.0',
            u'method': u'scripting/scriptCancel',
            u'params': {
                u'operationId': u'e18b9538-a7ff-4502-9c33-ac63ed42e5a5'}}
        complete_event = {
            u'jsonrpc': u'2.0',
            u'method': u'scripting/scriptComplete',
            u'params': {
                u'operationId': u'e18b9538-a7ff-4502-9c33-ac63ed42e5a5'}}
        error_event = {
            u'jsonrpc': u'2.0',
            u'method': u'scripting/scriptError',
            u'params': {
                u'operationId': u'e18b9538-a7ff-4502-9c33-ac63ed42e5a5',
                u'message': u'Scripting error occured',
                u'diagnosticMessage': u'error occured during scripting'}}

        progress_notification = {
            u'jsonrpc': u'2.0',
            u'method': u'scripting/scriptProgressNotification',
            u'params': {
                u'operationId': u'e18b9538-a7ff-4502-9c33-ac63ed42e5a5',
                u'status': u'Completed',
                u'count': 3,
                u'totalCount': 12,
                u'scriptingObject': {
                    u'type': u'FullTextCatalog',
                    u'schema': u'null',
                    u'name': u'SampleFullTextCatalog'}}}

        plan_notification = {
            u'jsonrpc': u'2.0',
            u'method': u'scripting/scriptPlanNotification',
            u'params': {
                u'operationId': u'e18b9538-a7ff-4502-9c33-ac63ed42e5a5',
                u'databaseObjects': [
                    {
                        u'type': u'Database',
                        u'schema': u'null',
                        u'name': u'AdventureWorks2014'}],
                u'count': 10}}

        decoder = scripting.ScriptingResponseDecoder()

        cancel_decoded = decoder.decode_response(cancel_event)
        complete_decoded = decoder.decode_response(complete_event)
        error_decoded = decoder.decode_response(error_event)
        progress_notification_decoded = decoder.decode_response(
            progress_notification)
        plan_notification_decoded = decoder.decode_response(plan_notification)

        self.assertIsNotNone(cancel_decoded)
        self.assertIsNotNone(complete_decoded)
        self.assertIsNotNone(error_decoded)
        self.assertIsNotNone(progress_notification_decoded)
        self.assertIsNotNone(plan_notification_decoded)

    def test_scripting_response_decoder_invalid(self):
        """
            Verify decode invalid response.
        """
        cancel_event = {
            u'jsonrpc': u'2.0',
            u'method': u'query/queryCancelled',
            u'params': {
                u'operationId': u'e18b9538-a7ff-4502-9c33-ac63ed42e5a5'}}
        complete_event = {
            u'jsonrpc': u'2.0',
            u'method': u'connect/connectionComplete',
            u'params': {
                u'operationId': u'e18b9538-a7ff-4502-9c33-ac63ed42e5a5'}}

        decoder = scripting.ScriptingResponseDecoder()

        cancel_decoded = decoder.decode_response(cancel_event)
        complete_decoded = decoder.decode_response(complete_event)

        # both events should remain untouched.
        self.assertTrue(isinstance(cancel_decoded, dict))
        self.assertTrue(isinstance(complete_decoded, dict))

    def test_default_script_options(self):
        """
            Verify default scripting options created.
        """
        scripting_options = scripting.ScriptingOptions()
        expected = {
            u'ANSIPadding': False,
            u'AppendToFile': False,
            u'CheckForObjectExistence': False,
            u'ContinueScriptingOnError': False,
            u'ConvertUDDTsToBaseTypes': False,
            u'GenerateScriptForDependentObjects': False,
            u'IncludeDescriptiveHeaders': False,
            u'IncludeSystemConstraintNames': False,
            u'IncludeUnsupportedStatements': False,
            u'SchemaQualifyObjectNames': False,
            u'ScriptBindings': False,
            u'SciptionCollations': False,
            u'ScriptDefaults': False,
            u'ScriptExtendedProperties': False,
            u'ScriptLogins': False,
            u'ScriptObjectLevelPermissions': False,
            u'ScriptOwner': False,
            u'ScriptUseDatabase': False,
            u'ScriptChangeTracking': False,
            u'ScriptCheckConstraints': False,
            u'ScriptDataCompressionOptions': False,
            u'ScriptForeignKey': False,
            u'ScriptFullTextIndexrs': False,
            u'ScriptIndexes': False,
            u'ScriptPrimaryKeys': False,
            u'ScriptTriggers': False,
            u'ScriptUniqueKeys': False,
            u'TypeOfDataToScript': u'SchemaOnly',
            u'ScriptDropAndCreate': u'ScriptCreate',
            u'ScriptForTheDatabaseEngineType': u'SingleInstance',
            u'ScriptStatistics': u'ScriptStatsNone',
            u'ScriptForServerVersion': u'SQL Server vNext CTP 1.0',
            u'ScriptForTheDatabaseEngineEdition': u'Microsoft SQL Server Standard Edition'}

        self.assertEqual(scripting_options.get_options(), expected)

    def test_nondefault_script_options(self):
        """
            Verify scripting options updated.
        """
        new_options = {
            u'ANSIPadding': True,
            u'AppendToFile': True,
            u'TypeOfDataToScript': u'SchemaOnly',
            u'ScriptDropAndCreate': u'ScriptCreate',
            u'ScriptForTheDatabaseEngineType': u'SingleInstance',
            u'ScriptStatistics': u'ScriptStatsNone',
            u'ScriptForServerVersion': u'SQL Server vNext CTP 1.0',
            u'ScriptForTheDatabaseEngineEdition': u'Microsoft SQL Server Standard Edition'}
        scripting_options = scripting.ScriptingOptions(new_options)

        expected = {
            u'ANSIPadding': True,
            u'AppendToFile': True,
            u'CheckForObjectExistence': False,
            u'ContinueScriptingOnError': False,
            u'ConvertUDDTsToBaseTypes': False,
            u'GenerateScriptForDependentObjects': False,
            u'IncludeDescriptiveHeaders': False,
            u'IncludeSystemConstraintNames': False,
            u'IncludeUnsupportedStatements': False,
            u'SchemaQualifyObjectNames': False,
            u'ScriptBindings': False,
            u'SciptionCollations': False,
            u'ScriptDefaults': False,
            u'ScriptExtendedProperties': False,
            u'ScriptLogins': False,
            u'ScriptObjectLevelPermissions': False,
            u'ScriptOwner': False,
            u'ScriptUseDatabase': False,
            u'ScriptChangeTracking': False,
            u'ScriptCheckConstraints': False,
            u'ScriptDataCompressionOptions': False,
            u'ScriptForeignKey': False,
            u'ScriptFullTextIndexrs': False,
            u'ScriptIndexes': False,
            u'ScriptPrimaryKeys': False,
            u'ScriptTriggers': False,
            u'ScriptUniqueKeys': False,
            u'TypeOfDataToScript': u'SchemaOnly',
            u'ScriptDropAndCreate': u'ScriptCreate',
            u'ScriptForTheDatabaseEngineType': u'SingleInstance',
            u'ScriptStatistics': u'ScriptStatsNone',
            u'ScriptForServerVersion': u'SQL Server vNext CTP 1.0',
            u'ScriptForTheDatabaseEngineEdition': u'Microsoft SQL Server Standard Edition'}

        self.assertEqual(scripting_options.get_options(), expected)

    def test_invalid_script_options(self):
        """
            Verify invalid script options.
        """
        invalid_options = {u'ANSIPadding': u'NonValid'}

        invalid_server_version = {
            u'ScriptForServerVersion': u'SQL Server 1689'}

        with self.assertRaises(ValueError):
            scripting.ScriptingOptions(invalid_options)
        with self.assertRaises(ValueError):
            scripting.ScriptingOptions(invalid_server_version)

    def test_script_database_params_format(self):
        """
            Verify scripting parameters format.
        """
        params = {
            u'FilePath': u'C:\temp\sample_db.sql',
            u'ConnectionString': u'Sample_connection_string',
            u'IncludeObjectCriteria': [],
            u'ExcludeObjectCriteria': [],
            u'DatabaseObjects': [u'Person.Person']}
        scripting_params = scripting.ScriptingParams(params)

        formatted_params = scripting_params.format()
        expected_script_options = {
            u'ANSIPadding': False,
            u'AppendToFile': False,
            u'CheckForObjectExistence': False,
            u'ContinueScriptingOnError': False,
            u'ConvertUDDTsToBaseTypes': False,
            u'GenerateScriptForDependentObjects': False,
            u'IncludeDescriptiveHeaders': False,
            u'IncludeSystemConstraintNames': False,
            u'IncludeUnsupportedStatements': False,
            u'SchemaQualifyObjectNames': False,
            u'ScriptBindings': False,
            u'SciptionCollations': False,
            u'ScriptDefaults': False,
            u'ScriptExtendedProperties': False,
            u'ScriptLogins': False,
            u'ScriptObjectLevelPermissions': False,
            u'ScriptOwner': False,
            u'ScriptUseDatabase': False,
            u'ScriptChangeTracking': False,
            u'ScriptCheckConstraints': False,
            u'ScriptDataCompressionOptions': False,
            u'ScriptForeignKey': False,
            u'ScriptFullTextIndexrs': False,
            u'ScriptIndexes': False,
            u'ScriptPrimaryKeys': False,
            u'ScriptTriggers': False,
            u'ScriptUniqueKeys': False,
            u'TypeOfDataToScript': u'SchemaOnly',
            u'ScriptDropAndCreate': u'ScriptCreate',
            u'ScriptForTheDatabaseEngineType': u'SingleInstance',
            u'ScriptStatistics': u'ScriptStatsNone',
            u'ScriptForServerVersion': u'SQL Server vNext CTP 1.0',
            u'ScriptForTheDatabaseEngineEdition': u'Microsoft SQL Server Standard Edition'}

        self.assertEqual(
            formatted_params[u'FilePath'],
            u'C:\temp\sample_db.sql')
        self.assertEqual(
            formatted_params[u'ConnectionString'],
            u'Sample_connection_string')
        # Reenable assertion below when the option is supported.
        #self.assertEqual(formatted_params['DatabaseObjects'], ['Person.Person'])
        self.assertEqual(
            formatted_params[u'ScriptOptions'],
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
            Helper to verify expected response count from a request.
        """
        progress_notification_event = 0
        complete_event = 0
        response_event = 0
        plan_notification_event = 0
        error_event = 0
        request.execute()

        while not request.completed():
            response = request.get_response()
            if func:
                func(self, response)
            if response:
                if isinstance(response, scripting.ScriptProgressNotificationEvent):
                    progress_notification_event += 1
                elif isinstance(response, scripting.ScriptCompleteEvent):
                    complete_event += 1
                elif isinstance(response, scripting.ScriptResponse):
                    response_event += 1
                elif isinstance(response, scripting.ScriptPlanNotificationEvent):
                    plan_notification_event += 1
                elif isinstance(response, scripting.ScriptErrorEvent):
                    error_event += 1

        self.assertEqual(response_event, response_count)
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
                u'..',
                u'scripting_baselines',
                file_name))


if __name__ == u'__main__':
    unittest.main()
