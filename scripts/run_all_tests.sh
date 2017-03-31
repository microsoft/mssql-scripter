#!/usr/bin/env bash
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

coverage erase
coverage run -a --concurrency=thread -m unittest discover -s ../mssql-scripter/mssql/common/tests
coverage run -a --concurrency=thread -m unittest discover -s ../mssql-scripter/mssql/contracts/tests
coverage run -a --concurrency=thread -m unittest discover -s ../mssql-scripter/mssql/tests

coverage report -m
