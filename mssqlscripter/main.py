# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import io
import os
import subprocess
import sys
import tempfile
import time


import mssqlscripter.scripterlogging
import mssqlscripter.argparser as parser
import mssqlscripter.scriptercallbacks as scriptercallbacks
import mssqlscripter.sqltoolsclient as sqltoolsclient
import mssqlscripter.utility as utility
import mssqltoolsservice

def main(args):
    """
        Main entry point to mssql-scripter.

    """
    parameters = parser.parse_arguments(args)

    temp_file_path = None
    if not parameters.FilePath:
        # Generate and track the temp file.
        temp_file_path = tempfile.NamedTemporaryFile(
            prefix=u'mssqlscripter_', delete=False).name
        parameters.FilePath = temp_file_path

    mssqltoolsservice_program = mssqltoolsservice.get_mssqltoolsservice_program()

    try:
        # Start mssqltoolsservice program.
        tools_service_process = subprocess.Popen(
            [
                mssqltoolsservice_program,
                u'--enable-logging'],
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

        with io.open(parameters.FilePath, encoding=u'utf-16') as script_file:
            for line in script_file.readlines():
                # If piping, stdout encoding is none in python 2 which resolves to 'ascii'.
                # If it is not none then the user has specified a custom
                # encoding.
                if not sys.stdout.encoding:
                    # We are piping and the user is using the default encoding,
                    # so encode to utf8.
                    line = line.encode(u'utf-8')
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
