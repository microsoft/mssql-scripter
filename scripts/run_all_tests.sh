#!/usr/bin/env bash
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

coverage run --concurrency=thread -m unittest discover -s ../src/common/tests
coverage run --concurrency=thread -m unittest discover -s ../src/mssql/requests/tests

coverage report -m