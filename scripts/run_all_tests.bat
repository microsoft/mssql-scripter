@echo off

REM --------------------------------------------------------------------------------------------
REM Copyright (c) Microsoft Corporation. All rights reserved.
REM Licensed under the MIT License. See License.txt in the project root for license information.
REM --------------------------------------------------------------------------------------------

coverage erase
coverage run -a --concurrency=thread -m unittest discover -s ../mssql-scripter/mssql/common/tests
coverage run -a --concurrency=thread -m unittest discover -s ../mssql-scripter/mssql/contracts/tests
coverage run -a --concurrency=thread -m unittest discover -s ../mssql-scripter/mssql/tests

coverage report -m
