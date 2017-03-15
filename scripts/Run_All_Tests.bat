@echo off

REM --------------------------------------------------------------------------------------------
REM Copyright (c) Microsoft Corporation. All rights reserved.
REM Licensed under the MIT License. See License.txt in the project root for license information.
REM --------------------------------------------------------------------------------------------

python -m unittest discover -s ../src/common/tests
python -m unittest discover -s ../src/mssql/scripter/tests

coverage run --concurrency=thread -m unittest discover -s ../src/common/tests
coverage report -m