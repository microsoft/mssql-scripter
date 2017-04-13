@echo off

REM --------------------------------------------------------------------------------------------
REM Copyright (c) Microsoft Corporation. All rights reserved.
REM Licensed under the MIT License. See License.txt in the project root for license information.
REM --------------------------------------------------------------------------------------------

coverage erase
coverage run -a --concurrency=thread -m unittest discover -s mssqlscripter/jsonrpc/tests
coverage run -a --concurrency=thread -m unittest discover -s mssqlscripter/jsonrpc/contracts/tests
coverage run -a --concurrency=thread -m unittest discover -s mssqlscripter/tests

coverage report -m
