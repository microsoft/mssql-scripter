# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import argparse
import getpass
import mssqlscripter
import os
import sys

MSSQL_SCRIPTER_CONNECTION_STRING = u'MSSQL_SCRIPTER_CONNECTION_STRING'
MSSQL_SCRIPTER_PASSWORD = u'MSSQL_SCRIPTER_PASSWORD'


def parse_arguments(args):
    """
        Initialize parser with scripter options.
    """
    parser = argparse.ArgumentParser(
        prog=u'mssql-scripter',
        description=u'Microsoft SQL Server Scripter Command Line Tool. ' +
            'Version {}'.format(mssqlscripter.__version__))

    group_connection_options = parser.add_mutually_exclusive_group()
    group_connection_options.add_argument(
        u'--connection-string',
        dest=u'ConnectionString',
        metavar=u'',
        help=u'Connection string of database to script')
    group_connection_options.add_argument(
        u'-S', u'--server',
        dest=u'Server',
        metavar=u'',
        help=u'Server name.')

    parser.add_argument(
        u'-d', u'--database',
        dest=u'Database',
        metavar=u'',
        help=u'Database name.')

    parser.add_argument(
        u'-U', u'--user',
        dest=u'UserId',
        metavar=u'',
        help=u'Login ID for server.')

    parser.add_argument(
        u'-P', u'--password',
        dest=u'Password',
        metavar=u'',
        help=u'Password.')

    # Basic parameters.
    parser.add_argument(
        u'-f', u'--file',
        dest=u'FilePath',
        metavar=u'',
        default=None,
        help=u'Output file name.',
    )

    parser.add_argument(
        u'--include-objects',
        dest=u'IncludeObjects',
        nargs=u'*',
        type=str,
        metavar=u'',
        help=u'Database objects to include in script.')

    parser.add_argument(
        u'--exclude-objects',
        dest=u'ExcludeObjects',
        nargs=u'*',
        type=str,
        metavar=u'',
        help=u'Database objects to exclude from script.')

    # General boolean Scripting Options
    parser.add_argument(
        u'--ansi-padding',
        dest=u'ANSIPadding',
        action=u'store_true',
        default=False,
        help=u'Generates ANSI Padding statements.')

    parser.add_argument(
        u'--append',
        dest=u'AppendToFile',
        action=u'store_true',
        default=False,
        help=u'Append script to file.')

    parser.add_argument(
        u'--check-for-existence',
        action=u'store_true',
        default=False,
        help=u'Check for database object existence.')

    parser.add_argument(
        u'-r',
        u'--continue-on-error',
        dest=u'ContinueScriptingOnError',
        action=u'store_true',
        default=False,
        help=u'Continue scripting on error.')

    parser.add_argument(
        u'--convert-uddts',
        dest=u'ConvertUDDTsToBaseTypes',
        action=u'store_true',
        default=False,
        help=u'Convert user-defined data types to base types.')

    parser.add_argument(
        u'--include-dependencies',
        dest=u'GenerateScriptForDependentObjects',
        action=u'store_true',
        default=False,
        help=u'Generate script for the dependent objects for each object scripted.')

    parser.add_argument(
        u'--headers',
        dest=u'IncludeDescriptiveHeaders',
        action=u'store_true',
        default=False,
        help=u'Include descriptive headers for each object scripted.')

    parser.add_argument(
        u'--constraint-names',
        dest=u'IncludeSystemConstraintNames',
        action=u'store_true',
        default=False,
        help=u'Include system constraint names to enforce declarative referential integrity.')

    parser.add_argument(
        u'--unsupported-statements',
        dest=u'IncludeUnsupportedStatements',
        action=u'store_true',
        default=False,
        help=u'Include statements in the script that are not supported on the target SQL Server Version.')

    parser.add_argument(
        u'--object-schema',
        dest=u'SchemaQualifyObjectNames',
        action=u'store_true',
        default=False,
        help=u'Prefix object names with the object schema.')

    parser.add_argument(
        u'--bindings',
        dest=u'ScriptBindings',
        action=u'store_true',
        default=False,
        help=u'Script options to set binding options.')

    parser.add_argument(
        u'--collation',
        dest=u'ScriptCollations',
        action=u'store_true',
        default=False,
        help=u'Script the objects that use collation.')

    parser.add_argument(
        u'--defaults',
        dest=u'ScriptDefaults',
        action=u'store_true',
        default=False,
        help=u'Script the default values.')

    parser.add_argument(
        u'--extended-properties',
        dest=u'ScriptExtendedProperties',
        action=u'store_true',
        default=False,
        help=u'Script the extended properties for each object scripted.')

    parser.add_argument(
        u'--logins',
        dest=u'ScriptLogins',
        action=u'store_true',
        default=False,
        help=u'Script all logins available on the server, passwords will not be scripted.')

    parser.add_argument(
        u'--object-permissions',
        dest=u'ScriptObjectLevelPermissions',
        action=u'store_true',
        default=False,
        help=u'Generate object-level permissions.')

    parser.add_argument(
        u'--owner',
        dest=u'ScriptOwner',
        action=u'store_true',
        default=False,
        help=u'Script owner for the objects.')

    parser.add_argument(
        u'--use-database',
        dest=u'ScriptUseDatabase',
        action=u'store_true',
        default=False,
        help=u'Generate USE DATABASE statement.')

    group_type_of_data = parser.add_mutually_exclusive_group()
    group_type_of_data.add_argument(
        u'--schema-only',
        dest=u'TypeOfDataToScript',
        action=u'store_const',
        const=u'SchemaOnly',
        default=u'SchemaOnly',
        help=u'Generate scripts that contains schema only.')
    group_type_of_data.add_argument(
        u'--data-only',
        dest=u'TypeOfDataToScript',
        action=u'store_const',
        const=u'DataOnly',
        default=u'SchemaOnly',
        help=u'Generate scripts that contains data only.')
    group_type_of_data.add_argument(
        u'--schema-and-data',
        dest=u'TypeOfDataToScript',
        action=u'store_const',
        const=u'SchemaAndData',
        default=u'SchemaOnly',
        help=u'Generate scripts that contain schema and data.')

    group_create_drop = parser.add_mutually_exclusive_group()
    group_create_drop.add_argument(
        u'--script-create',
        dest=u'ScriptCreate',
        action=u'store_const',
        const=u'ScriptCreate',
        default=u'ScriptCreate',
        help=u'Script object CREATE statements.')
    group_create_drop.add_argument(
        u'--script-drop',
        dest=u'ScriptCreate',
        action=u'store_const',
        const=u'ScriptDrop',
        default=u'ScriptCreate',
        help=u'Script object DROP statements')
    group_create_drop.add_argument(
        u'--script-drop-create',
        dest=u'ScriptCreate',
        action=u'store_const',
        const=u'ScriptCreateDrop',
        default=u'ScriptCreate',
        help=u'Script object CREATE and DROP statements.')

    parser.add_argument(
        u'--statistics',
        dest=u'ScriptStatistics',
        action=u'store_const',
        const=u'ScriptStatsAll',
        default=u'ScriptStatsNone',
        help=u'Script all statistics.')

    parser.add_argument(
        u'--target-server-version',
        dest=u'ScriptForServerVersion',
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
        default=u'2016',
        help=u'Script only features compatible with the specified SQL Version.')

    parser.add_argument(
        u'--target-server-edition',
        dest=u'ScriptForTheDatabaseEngineEdition',
        choices=[
            u'Standard',
            u'Personal'
            u'Express',
            u'Enterprise',
            u'Stretch'],
        default=u'Enterprise',
        help=u'Script only features compatible with the specified SQL Server database edition.')

    parser.add_argument(
        u'--database-engine-type',
        dest=u'ScriptForTheDatabaseEngineType', 
        # This parameter is determined based on engine edition and version in
        # the background. User cannot select it.
        action=u'store_const',
        const=u'SingleInstance',
        default=u'SingleInstance',
        help=argparse.SUPPRESS)

    # Table/View Options
    parser.add_argument(
        u'--change-tracking',
        dest=u'ScriptChangeTracking',
        action=u'store_true',
        default=False,
        help=u'Script the change tracking information.')

    parser.add_argument(
        u'--check-constraints',
        dest=u'ScriptCheckConstraints',
        action=u'store_true',
        default=False,
        help=u'Script the check constraints for each table or view scripted.')

    parser.add_argument(
        u'--data-compressions',
        dest=u'ScriptDataCompressionOptions',
        action=u'store_true',
        default=False,
        help=u'Script the data compression information.')

    parser.add_argument(
        u'--foreign-keys',
        dest=u'ScriptForeignKey',
        action=u'store_true',
        default=False,
        help=u'Script the foreign keys for each table scripted.')

    parser.add_argument(
        u'--full-text-indexes',
        dest=u'ScriptFullTextIndexes',
        action=u'store_true',
        default=False,
        help=u'Script the full-text indexes for each table or indexed view scripted.')

    parser.add_argument(
        u'--indexes',
        dest=u'ScriptIndexes',
        action=u'store_true',
        default=False,
        help=u'Script the indexes (XML and clustered) for each table or indexed view scripted.')

    parser.add_argument(
        u'--primary-keys',
        dest=u'ScriptPrimaryKeys',
        action=u'store_true',
        default=False,
        help=u'Script the primary keys for each table or view scripted.')

    parser.add_argument(
        u'--triggers',
        dest=u'ScriptTriggers',
        action=u'store_true',
        default=False,
        help=u'Script the triggers for each table or view scripted.')

    parser.add_argument(
        u'--unique-keys',
        dest=u'ScriptUniqueKeys',
        action=u'store_true',
        default=False,
        help=u'Script the unique keys for each table or view scripted.')

    # Configuration Options.
    parser.add_argument(
        u'--display-progress',
        dest=u'DisplayProgress',
        action=u'store_true',
        default=False,
        help=u'Display scripting progress.')

    parser.add_argument(
        u'--enable-toolsservice-logging',
        dest=u'EnableLogging',
        action=u'store_true',
        default=False,
        help=u'Enable verbose logging.')

    parser.add_argument(
    u'--version',
    action=u'version',
    version='{}'.format(mssqlscripter.__version__))

    parameters = parser.parse_args(args)
    
    if parameters.Server:
        build_connection_string(parameters)
    elif parameters.ConnectionString is None:
        # Check environment variable for connection string.
        if not get_connection_string_from_environment(parameters):
            sys.stdout.write(u'Please specify connection information using --connection-string or --server and/or --database --user\n')
            sys.exit()

    map_server_options(parameters)

    return parameters

def get_connection_string_from_environment(parameters):
    """
        Get connection string from environment variable.
    """
    if MSSQL_SCRIPTER_CONNECTION_STRING in os.environ:
        parameters.ConnectionString = os.environ[MSSQL_SCRIPTER_CONNECTION_STRING]
        return True

    return False


def build_connection_string(parameters):
    """
        Build connection string.
    """
    connection_string = u'Server={};'.format(parameters.Server)
    if parameters.Database:
        connection_string += u'Database={};'.format(parameters.Database)

    # Standard connection if user id is supplied.
    if parameters.UserId:
        connection_string += u'User Id={};'.format(parameters.UserId)
        # If no password supplied, check for environment variable.
        if parameters.Password is None and MSSQL_SCRIPTER_PASSWORD in os.environ:
            parameters.Password = os.environ[MSSQL_SCRIPTER_PASSWORD ]

        connection_string += u'Password={};'.format(parameters.Password or getpass.getpass())
    
    else:
        connection_string += u'Integrated Security=True;'

    parameters.ConnectionString = connection_string


def map_server_options(parameters):
    """
        Map short form to long form name and maps Azure versions to their appropriate editions.
    """
    azure_server_edition_map = {
        u'AzureDB': u'Microsoft Azure SQL Database Edition',
        u'AzureDW': u'Microsoft Azure Data Warehouse Edition',
    }

    on_prem_server_edition_map = {
        u'Standard': u'Microsoft SQL Server Standard Edition',
        u'Personal': u'Microsoft SQL Server Personal Edition',
        u'Express': u'Microsoft SQL Server Express Edition',
        u'Enterprise': u'Microsoft SQL Server Enterprise Edition',
        u'Stretch': u'Microsoft SQL Server Stretch Database Edition',
    }

    on_prem_server_version_map = {
        u'2005': u'SQL Server 2005',
        u'2008': u'SQL Server 2008',
        u'2008R2': u'SQL Server 2008 R2',
        u'2012': u'SQL Server 2012',
        u'2014': u'SQL Server 2014',
        u'2016': u'SQL Server 2016',
        u'vNext': u'SQL Server vNext CTP',
    }

    target_server_version = parameters.ScriptForServerVersion
    target_server_edition = parameters.ScriptForTheDatabaseEngineEdition
    # When targetting Azure, only the edition matters.
    if u'Azure' in target_server_version:
        # SMO ignores this value when it is targetting Azure.
        parameters.ScriptForServerVersion = u'SQL Server 2016'
        parameters.ScriptForTheDatabaseEngineEdition = azure_server_edition_map[
            target_server_version]
        parameters.ScriptForTheDatabaseEngineType = u'SqlAzure'

    else:
        parameters.ScriptForServerVersion = on_prem_server_version_map[target_server_version]
        parameters.ScriptForTheDatabaseEngineEdition = on_prem_server_edition_map[
            target_server_edition]
        parameters.ScriptForTheDatabaseEngineType = u'SingleInstance'

    return parameters
