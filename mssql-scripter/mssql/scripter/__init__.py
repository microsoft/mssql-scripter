# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import argparse
import os
import platform
import site
import sys


# Check repo if in dev mode.
TOOLS_SERVICE_DIR = os.path.abspath(
    os.path.join(
        os.path.abspath(__file__),
        '..',
        '..',
        'sqltoolsservice'))
if (not os.path.exists(TOOLS_SERVICE_DIR)):
    # Production mode.
    for path in site.getsitepackages():
        if (path.endswith('site-packages')):
            TOOLS_SERVICE_DIR = os.path.join(path, 'mssql', 'sqltoolsservice')
            break


def get_sql_tools_service_path():
    """
        Retrieves Sql tools service program path.
    """
    sql_tools_service_file_name = 'Microsoft.SqlTools.ServiceLayer{}'.format(
        '.exe' if (platform.system() == 'Windows') else '')

    sql_tools_service_path = os.path.join(
        TOOLS_SERVICE_DIR, sql_tools_service_file_name)

    if (not os.path.exists(sql_tools_service_path)):
        raise EnvironmentError(
            '{} does not exist. mssql-scripter may be corrupted, please reinstall.'.format(sql_tools_service_path))

    return sql_tools_service_path


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

    response_handlers = {
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
        prog='mssql-scripter',
        description='mssql-scripter tool used for scripting out databases')

    parser.add_argument(
        'ConnectionString',
        help='Connection string of database to script')

    parser.add_argument(
        '-f', '--file',
        dest='FilePath',
        metavar='',
        help='',
        default=None)

    # General boolean Scripting Options
    parser.add_argument(
        '--ansi-padding',
        dest='ANSIPadding',
        action='store_true',
        help='',
        default=False)
    parser.add_argument(
        '--append',
        dest='AppendToFile',
        action='store_true',
        help='',
        default=False)
    parser.add_argument(
        '--CheckForObjectExistence',
        action='store_true',
        help='',
        default=False)
    parser.add_argument(
        '-r',
        '--continue-on-error',
        dest='ContinueScriptingOnError',
        action='store_true',
        help='',
        default=False)
    parser.add_argument(
        '--convert-uddts',
        dest='ConvertUDDTsToBaseTypes',
        action='store_true',
        help='',
        default=False)
    parser.add_argument(
        '--include-dependencies',
        dest='GenerateScriptForDependentObjects',
        action='store_true',
        help='',
        default=False)
    parser.add_argument(
        '--headers',
        dest='IncludeDescriptiveHeaders',
        action='store_true',
        help='',
        default=False)
    parser.add_argument(
        '--constraint-names',
        dest='IncludeSystemConstraintNames',
        action='store_true',
        help='',
        default=False)
    parser.add_argument(
        '--unsupported-statements',
        dest='IncludeUnsupportedStatements',
        action='store_true',
        help='',
        default=False)
    parser.add_argument(
        '--object-schema',
        dest='SchemaQualifyObjectNames',
        action='store_true',
        help='',
        default=False)
    parser.add_argument(
        '--bindings',
        dest='ScriptBindings',
        action='store_true',
        help='',
        default=False)
    parser.add_argument(
        '--collation',
        dest='ScriptCollations',
        action='store_true',
        help='',
        default=False)
    parser.add_argument(
        '--defaults',
        dest='ScriptDefaults',
        action='store_true',
        help='',
        default=False)
    parser.add_argument(
        '--extended-properties',
        dest='ScriptExtendedProperties',
        action='store_true',
        help='',
        default=False)
    parser.add_argument(
        '--logins',
        dest='ScriptLogins',
        action='store_true',
        help='',
        default=False)
    parser.add_argument(
        '--object-permissions',
        dest='ScriptObjectLevelPermissions',
        action='store_true',
        help='',
        default=False)
    parser.add_argument(
        '--owner',
        dest='ScriptOwner',
        action='store_true',
        help='',
        default=False)
    parser.add_argument(
        '--use-database',
        dest='ScriptUseDatabase',
        action='store_true',
        help='',
        default=False)

    group_type_of_data = parser.add_mutually_exclusive_group()
    group_type_of_data.add_argument(
        '--schema-only',
        dest='TypeOfDataToScript',
        action='store_const',
        const='SchemaOnly',
        default='SchemaOnly')
    group_type_of_data.add_argument(
        '--data-only',
        dest='TypeOfDataToScript',
        action='store_const',
        const='DataOnly',
        default='SchemaOnly')
    group_type_of_data.add_argument(
        '--schema-and-data',
        dest='TypeOfDataToScript',
        action='store_const',
        const='SchemaAndData',
        default='SchemaOnly')

    group_create_drop = parser.add_mutually_exclusive_group()
    group_create_drop.add_argument(
        '--script-create',
        dest='ScriptCreate',
        action='store_const',
        const='ScriptCreate',
        default='ScriptCreate')
    group_create_drop.add_argument(
        '--script-drop',
        dest='ScriptCreate',
        action='store_const',
        const='ScriptDrop',
        default='ScriptCreate')
    group_create_drop.add_argument(
        '--script-drop-create',
        dest='ScriptCreate',
        action='store_const',
        const='ScriptCreateDrop',
        default='ScriptCreate')

    parser.add_argument(
        '--statistics',
        dest='ScriptStatistics',
        action='store_const',
        const='ScriptStatsAll',
        default='ScriptStatsNone')

    parser.add_argument(
        '--target-server-version',
        dest='ScriptForServerVersion',
        choices=[
            '2005',
            '2008',
            '2008R2',
            '2012',
            '2014',
            '2016',
            'vNext',
            'AzureDB',
            'AzureDW'],
        default='2016')

    parser.add_argument(
        '--target-server-edition',
        dest='ScriptForTheDatabaseEngineEdition',
        choices=[
            'Standard',
            'Personal'
            'Express',
            'Enterprise',
            'Stretch'],
        default='Enterprise')
    parser.add_argument(
        '--database-engine-type',
        dest='ScriptForTheDatabaseEngineType',
        help=argparse.SUPPRESS,
        # This parameter is determined based on engine edition and version in
        # the background. User cannot select it.
        action='store_const',
        const='SingleInstance',
        default='SingleInstance'
    )
    # Table/View Options
    parser.add_argument(
        '--change-tracking',
        dest='ScriptChangeTracking',
        action='store_true',
        help='',
        default=False)
    parser.add_argument(
        '--check-constraints',
        dest='ScriptCheckConstraints',
        action='store_true',
        help='',
        default=False)
    parser.add_argument(
        '--data-compressions',
        dest='ScriptDataCompressionOptions',
        action='store_true',
        help='',
        default=False)
    parser.add_argument(
        '--foreign-keys',
        dest='ScriptForeignKey',
        action='store_true',
        help='',
        default=False)
    parser.add_argument(
        '--full-text-indexes',
        dest='ScriptFullTextIndexes',
        action='store_true',
        help='',
        default=False)
    parser.add_argument(
        '--indexes',
        dest='ScriptIndexes',
        action='store_true',
        help='',
        default=False)
    parser.add_argument(
        '--primary-keys',
        dest='ScriptPrimaryKeys',
        action='store_true',
        help='',
        default=False)
    parser.add_argument(
        '--triggers',
        dest='ScriptTriggers',
        action='store_true',
        help='',
        default=False)
    parser.add_argument(
        '--unique-keys',
        dest='ScriptUniqueKeys',
        action='store_true',
        help='',
        default=False)

    # Configuration Options
    parser.add_argument(
        '--display-progress',
        dest='DisplayProgress',
        action='store_true',
        help='',
        default=False)
    # We can toggle logging in the future once we refactor it into it's own module
    # parser.add_argument('-GenerateLog', default=False)

    return parser


def map_server_options(parameters):
    """
        Maps short form to long form name and maps Azure versions to their appropriate editions.
    """
    azure_server_edition_map = {
        'AzureDB': 'Microsoft Azure SQL Database Edition',
        'AzureDW': 'Microsoft Azure Data Warehouse Edition',
    }

    on_prem_server_edition_map = {
        'Standard': 'Microsoft SQL Server Standard Edition',
        'Personal': 'Microsoft SQL Server Personal Edition',
        'Express': 'Microsoft SQL Server Express Edition',
        'Enterprise': 'Microsoft SQL Server Enterprise Edition',
        'Stretch': 'Microsoft SQL Server Stretch Database Edition',
    }

    on_prem_server_version_map = {
        '2005': 'SQL Server 2005',
        '2008': 'SQL Server 2008',
        '2008R2': 'SQL Server 2008 R2',
        '2012': 'SQL Server 2012',
        '2014': 'SQL Server 2014',
        '2016': 'SQL Server 2016',
        'vNext': 'SQL Server vNext CTP',
    }

    target_server_version = parameters.ScriptForServerVersion
    target_server_edition = parameters.ScriptForTheDatabaseEngineEdition
    # When targetting Azure, only the edition matters.
    if ('Azure' in target_server_version):
        # SMO ignores this value when it is targetting Azure.
        parameters.ScriptForServerVersion = 'SQL Server 2016'
        parameters.ScriptForTheDatabaseEngineEdition = azure_server_edition_map[
            target_server_version]
        parameters.ScriptForTheDatabaseEngineType = 'SqlAzure'

    else:
        parameters.ScriptForServerVersion = on_prem_server_version_map[target_server_version]
        parameters.ScriptForTheDatabaseEngineEdition = on_prem_server_edition_map[
            target_server_edition]
        parameters.ScriptForTheDatabaseEngineType = 'SingleInstance'

    return parameters
