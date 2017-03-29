@echo off

REM --------------------------------------------------------------------------------------------
REM Copyright (c) Microsoft Corporation. All rights reserved.
REM Licensed under the MIT License. See License.txt in the project root for license information.
REM --------------------------------------------------------------------------------------------


coverage run --concurrency=thread -m unittest discover -s ../src/mssql/common/tests
coverage run --concurrency=thread -m unittest discover -s ../src/mssql/requests/tests
coverage report -m