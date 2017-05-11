# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import os
import utility


root_dir = os.path.abspath(os.path.join(os.path.abspath(__file__), '..'))
mssqlscripter_coverage_report_dir = os.path.abspath(os.path.join(root_dir, 'mssqlscripter', '*'))


def run_unittests_and_code_coverage():
    """
        Run all unit tests with code coverage.
    """
    utility.exec_command('coverage erase', root_dir)
    utility.exec_command(
        'coverage run -a --concurrency=thread -m unittest discover -s mssqlscripter/jsonrpc/tests',
        root_dir,
        continue_on_error=False
    )
    utility.exec_command(
        'coverage run -a --concurrency=thread -m unittest discover -s mssqlscripter/jsonrpc/contracts/tests',
        root_dir,
        continue_on_error=False
    )
    utility.exec_command(
        'coverage run -a --concurrency=thread -m unittest discover -s mssqlscripter/tests',
        root_dir,
        continue_on_error=False
    )
    utility.exec_command(
        'coverage report --include={}'.format(mssqlscripter_coverage_report_dir),
        root_dir,
        continue_on_error=False
    )
    utility.exec_command(
        'coverage xml'.format(mssqlscripter_coverage_report_dir),
        root_dir,
        continue_on_error=False
    )


if __name__ == '__main__':
    run_unittests_and_code_coverage()
