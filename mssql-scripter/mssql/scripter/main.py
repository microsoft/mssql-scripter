# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import io
import os
import subprocess
import sys

import mssql.scripter as scripter
from mssql.sql_tools_client import Sql_Tools_Client


def main(args):
    """
        Main entry point to mssql-scripter.

    """

    parser = scripter.initialize_parser()
    parameters = parser.parse_args(args)

    sql_tools_service_path = scripter.get_native_tools_service_path()

    # Start the tools Service
    tools_service_process = subprocess.Popen(
        [
            sql_tools_service_path,
            "--enable-logging"],
        bufsize=0,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE)

    # Python 2.7 uses the built-in File type when referencing the subprocess.PIPE.
    # This built-in type for that version blocks on readinto() because it attempts to fill buffer.
    # Wrap a FileIO around it to use a different implementation that does not attempt to fill the buffer
    # on readinto().
    std_out_wrapped = io.open(
        tools_service_process.stdout.fileno(),
        'rb',
        buffering=0,
        closefd=False)

    sql_tools_client = Sql_Tools_Client(
        tools_service_process.stdin,
        std_out_wrapped)

    scripting_request = sql_tools_client.create_request(
        'scripting_request', vars(parameters))
    scripting_request.execute()

    while(not scripting_request.completed()):
        response = scripting_request.get_response()

        if (response):
            scripter.handle_response(response, parameters.DisplayProgress)

    # Once the response is complete
    with io.open(parameters.FilePath, 'r', encoding='utf-16') as script_file:
        sys.stdout.write(script_file.read())

    # May need to add a timer here
    sql_tools_client.shutdown()
    tools_service_process.kill()


if __name__ == '__main__':
    main(sys.argv[1:])
