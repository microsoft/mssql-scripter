# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
import argparse
import os
import platform
import site
import sys
import tempfile


# Check repo if in dev mode.
TOOLS_SERVICE_DIR = os.path.abspath(os.path.join(os.path.abspath(__file__), '..', '..', 'sqltoolsservice'))
if (not os.path.exists(TOOLS_SERVICE_DIR)):
    # Production mode.
    TOOLS_SERVICE_DIR=site.getsitepackages()[0]

def get_native_tools_service_path():

    tools_service_program='Microsoft.SqlTools.ServiceLayer{}'.format('.exe'
        if (platform.system() == 'Windows') else '')

    return os.path.join(TOOLS_SERVICE_DIR, tools_service_program)

def handle_response(response, display=False):
    """
        Dispatches response to appropriate response handler based on response type.
    """
    # TODO: Revisit the format of the messages

    def handle_script_response(response, display=False):
        if (display):
            sys.stderr.write(
                'Scripting request submitted with request id: {0}\n'.format(
                    response.operation_id))

    def handle_script_error(response, display=False):
        # Always display error messages
        sys.stdout.write(
            'Scripting request: {0} encountered error: {1}\n'.format(
                response.operation_id, response.message))

    def handle_script_plan_notification(response, display=False):
        if (display):
            sys.stderr.write(
                'Scripting request: {0} plan: {1} database objects\n'.format(
                    response.operation_id, response.count))

    def handle_script_progress_notification(response, display=False):
        if (display):
            sys.stderr.write(
                'Scripting progress: Status: {0} Progress: {1} out of {2} objects scripted\n'.format(
                    response.status, response.count, response.total_count))

    def handle_script_complete(response, display=False):
        if (display):
            sys.stderr.write(
                'Scripting request: {0} completed\n'.format(
                    response.operation_id))

    response_handlers={
        'ScriptResponse': handle_script_response,
        'ScriptErrorEvent': handle_script_error,
        'ScriptPlanNotificationEvent': handle_script_plan_notification,
        'ScriptProgressNotificationEvent': handle_script_progress_notification,
        'ScriptCompleteEvent': handle_script_complete
    }

    response_name = type(response).__name__

    if (response_name in response_handlers):
        return response_handlers[response_name](response, display)


def initialize_parser():
    """
        Initializes the parser with supported scripting options.
    """
    parser = argparse.ArgumentParser(
        description='mssql-scripter tool used for scripting out databases')

    parser.add_argument(
        'ConnectionString',
        help='Connection string of database to script')
        
    parser.add_argument(
        'FilePath',
        help='target file to store the script of the database')

    # General boolean Scripting Options
    parser.add_argument('--ANSIPadding', help='', default=False)
    parser.add_argument('--AppendToFile', help='', default=False)
    parser.add_argument('--CheckForObjectExistence', default=False)
    parser.add_argument('--ContinueScriptingOnError', default=False)
    parser.add_argument('--ConvertUDDTsToBaseTypes', default=False)
    parser.add_argument('--GenerateScriptForDependentObjects', default=False)
    parser.add_argument('--IncludeDescriptiveHeaders', default=False)
    parser.add_argument('--IncludeSystemConstraintNames', default=False)
    parser.add_argument('--IncludeUnsupportedStatements', default=False)
    parser.add_argument('--SchemaQualifyObjectNames', default=False)
    parser.add_argument('--ScriptBindings', default=False)
    parser.add_argument('--SciptionCollations', default=False)
    parser.add_argument('--ScriptDefaults', default=False)
    parser.add_argument('--ScriptExtendedProperties', default=False)
    parser.add_argument('--ScriptLogins', default=False)
    parser.add_argument('--ScriptObjectLevelPermissions', default=False)
    parser.add_argument('--ScriptOwner', default=False)
    parser.add_argument('--ScriptUseDatabase', default=False)

    # Enum arguments
    parser.add_argument(
        '--TypeOfDataToScript',
        choices=[
            'SchemaAndData',
            'DataOnly',
            'SchemaOnly'],
        default='SchemaOnly')
    parser.add_argument(
        '--ScriptDropAndCreate',
        choices=[
            'ScriptCreate',
            'ScriptDrop',
            'ScriptCreateDrop'],
        default='ScriptCreate')
    parser.add_argument(
        '--ScriptForTheDatabaseEngineType',
        choices=[
            'SingleInstance',
            'SqlAzure'],
        default='SingleInstance')
    parser.add_argument(
        '--ScriptStatistics',
        choices=[
            'ScriptStatsAll',
            'ScriptStatsNone',
            'ScriptStatsDll'],
        default='ScriptStatsNone')
    parser.add_argument(
        '--ScriptForServerVersion',
        choices=[
            'SQL Server 2005',
            'SQL Server 2008',
            'SQL Server 2008 R2',
            'SQL Server 2012',
            'SQL Server 2014',
            'SQL Server 2016',
            'SQL Server vNext CTP 1.0'],
        default='SQL Server 2016')
    parser.add_argument(
        '--ScriptForTheDatabaseEngineEdition',
        choices=[
            'Microsoft SQL Server Standard Edition',
            'Microsoft SQL Server Personal Edition'
            'Microsoft SQL Server Express Edition',
            'Microsoft SQL Server Enterprise Edition',
            'Microsoft SQL Server Stretch Database Edition'],
        default='Microsoft SQL Server Standard Edition')

    # Table/View Options
    parser.add_argument('--ScriptChangeTracking', default=False)
    parser.add_argument('--ScriptCheckConstraints', default=False)
    parser.add_argument('--ScriptDataCompressionOptions', default=False)
    parser.add_argument('--ScriptForeignKey', default=False)
    parser.add_argument('--ScriptFullTextIndexrs', default=False)
    parser.add_argument('--ScriptIndexes', default=False)
    parser.add_argument('--ScriptPrimaryKeys', default=False)
    parser.add_argument('--ScriptTriggers', default=False)
    parser.add_argument('--ScriptUniqueKeys', default=False)

    # Configuration Options
    parser.add_argument('--DisplayProgress', default=False)
    # We can toggle logging in the future once we refactor it into it's own module
    # parser.add_argument('-GenerateLog', default=False)

    return parser
