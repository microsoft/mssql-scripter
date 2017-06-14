# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import copy
import io
import logging
import os
import platform
import subprocess
import sys
import tempfile
import time


import mssqlscripter.scripterlogging as scripterlogging
import mssqlscripter.argparser as parser
import mssqlscripter.scriptercallbacks as scriptercallbacks
import mssqlscripter.sqltoolsclient as sqltoolsclient
import mssqltoolsservice

logger = logging.getLogger(u'mssqlscripter.main')


def main(args):
    """
        Main entry point to mssql-scripter.
    """
    scripterlogging.initialize_logger()
    logger.info('Python Information :{}'.format(sys.version_info))
    logger.info('System Information: system={} architecture={} version={}'.format(platform.system(), platform.architecture()[0], platform.version()))

    parameters = parser.parse_arguments(args)
    scrubbed_parameters = copy.deepcopy(parameters)

    try:
        scrubbed_parameters.ConnectionString = '*******'
        scrubbed_parameters.Password = '********'
    except AttributeError:
        # Password was not given, using integrated auth.
        pass

    logger.info(scrubbed_parameters)

    temp_file_path = None
    if not parameters.FilePath and parameters.ScriptDestination is 'ToSingleFile':
        # Generate and track the temp file.
        temp_file_path = tempfile.NamedTemporaryFile(
            prefix=u'mssqlscripter_', delete=False).name
        parameters.FilePath = temp_file_path

    sqltoolsservice_args = [mssqltoolsservice.get_executable_path()]

    if parameters.EnableLogging:
        sqltoolsservice_args.append('--enable-logging')
        sqltoolsservice_args.append('--log-dir')
        sqltoolsservice_args.append(scripterlogging.get_config_log_dir())

    logger.debug('Loading mssqltoolsservice with arguments {}'.format(sqltoolsservice_args))
    try:
        # Start mssqltoolsservice program.
        tools_service_process = subprocess.Popen(
            sqltoolsservice_args,
            bufsize=0,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE)

        # Python 2.7 uses the built-in File type when referencing the subprocess.PIPE.
        # This built-in type for that version blocks on readinto() because it attempts to fill buffer.
        # Wrap a FileIO around it to use a different implementation that does not attempt to fill the buffer
        # on readinto().
        std_out_wrapped = io.open(
            tools_service_process.stdout.fileno(),
            u'rb',
            buffering=0,
            closefd=False)

        sql_tools_client = sqltoolsclient.SqlToolsClient(
            tools_service_process.stdin,
            std_out_wrapped)

        scripting_request = sql_tools_client.create_request(
            u'scripting_request', vars(parameters))
        scripting_request.execute()

        while not scripting_request.completed():
            response = scripting_request.get_response()

            if response:
                scriptercallbacks.handle_response(response, parameters.DisplayProgress)

        # Only write to stdout if user did not provide a file path.
        logger.info('stdout current encoding: {}'.format(sys.stdout.encoding))
        if temp_file_path:
            with io.open(parameters.FilePath, encoding=u'utf-16') as script_file:
                for line in script_file.readlines():
                    sys.stdout.write(line)

    finally:

        sql_tools_client.shutdown()
        tools_service_process.kill()
        # 1 second time out, allow tools service process to be killed.
        time.sleep(1)
        # None value indicates process has not terminated.
        if not tools_service_process.poll():
            sys.stderr.write(
                u'Sql Tools Service process was not shut down properly.')
        try:
            # Remove the temp file if we generated one.
            if temp_file_path:
                os.remove(temp_file_path)
        except Exception:
            # Suppress exceptions.
            pass


if __name__ == u'__main__':
    main(sys.argv[1:])
