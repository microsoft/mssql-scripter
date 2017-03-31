@echo off

REM --------------------------------------------------------------------------------------------
REM Copyright (c) Microsoft Corporation. All rights reserved.
REM Licensed under the MIT License. See License.txt in the project root for license information.
REM --------------------------------------------------------------------------------------------

coverage run --concurrency=thread -m unittest discover -s ../mssql-scripter/mssql/common/tests
coverage run --concurrency=thread -m unittest discover -s ../mssql-scripter/mssql/contracts/tests

coverage report -m