# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
import subprocess
import sys
import os.path
import io

from mssql.scripter import scripter_logging, handle_response, initialize_parser
from mssql.sql_tools_client import Sql_Tools_Client
from subprocess import PIPE


def main(args):
    """
        Main entry point to mssql-scripter.

    """

    parser = initialize_parser()
    parameters = parser.parse_args(args)

    # Resolve the path to the tool service
    basepath = os.path.dirname(__file__)
    tools_service_path = os.path.abspath(
        os.path.join(basepath, "..", "sqltoolsservice", "Microsoft.SqlTools.ServiceLayer"))
    
    # Start the tools Service
    tools_service_process = subprocess.Popen(
        [tools_service_path, "--enable-logging"],
        bufsize=0,
        stdin=PIPE,
        stdout=PIPE)

    # Wrap stdout from 2.7 compat
    stdout_wrapped = io.open(tools_service_process.stdout.fileno(), 'rb', closefd=False)

    # Start the sql_tools_client
    sql_tools_client = Sql_Tools_Client(
        tools_service_process.stdin,
        stdout_wrapped)

    # Create the scripting request
    scripting_request = sql_tools_client.create_request(
        'scripting_request', vars(parameters))
    scripting_request.execute()

    while(not scripting_request.completed()):
        # Process the responses
        response = scripting_request.get_response()
        if (response is not None and parameters.DisplayProgress):
            handle_response(response)

    # Once the response is complete
    with io.open(parameters.FilePath, 'r', encoding='utf-16') as script_file:
        sys.stdout.write(script_file.read())

    # May need to add a timer here
    sql_tools_client.shutdown()
    tools_service_process.kill()

if __name__ =='__main__':
    main()
