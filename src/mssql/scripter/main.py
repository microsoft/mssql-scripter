# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
import subprocess
import sys

from mssql.scripter import scripter_logging, handle_response, initialize_parser
from mssql.client import Sql_Tools_Client
from subprocess import PIPE


def main():
    """
        Main entry point to the MSSQL-Scripter.

    """
    # Initialize the parser
    parser = initialize_parser()
    # Parse the parameters
    parameters = parser.parse_args()

    # Start the tools Service
    # TODO: Add helper to find the actual install location
    tools_service_process = subprocess.Popen(
        [
            r"D:\repos\sql-xplat-cli\sqltoolsservice\Microsoft.SqlTools.ServiceLayer.exe",
            "--enable-logging"],
        bufsize=0,
        stdin=PIPE,
        stdout=PIPE)

    # Start the sql_tools_client
    sql_tools_client = Sql_Tools_Client(
        tools_service_process.stdin,
        tools_service_process.stdout)

    # Create the scripting request
    scripting_request = sql_tools_client.create_request_factory(
        'scripting_request', vars(parameters))
    scripting_request.execute()

    while(not scripting_request.completed()):
        # Process the responses
        response = scripting_request.get_response()
        if (response is not None and parameters.DisplayProgress):
            handle_response(response)

    # Once the response is complete
    with open(parameters.FilePath, 'r', encoding='utf-16') as script_file:
        sys.stdout.write(script_file.read())

    # May need to add a timer here
    sql_tools_client.shutdown()
    tools_service_process.kill()


if __name__ == "__main__":
    # execute only if run as a script
    main()
