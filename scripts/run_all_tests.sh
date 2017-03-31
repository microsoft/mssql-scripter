#!/usr/bin/env bash
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

<<<<<<< HEAD
coverage run --concurrency=thread -m unittest discover -s ../mssql-scripter/mssql/common/tests
coverage run --concurrency=thread -m unittest discover -s ../mssql-scripter/mssql/contracts/tests
=======
coverage run --concurrency=thread -m unittest discover -s ../src/common/tests
coverage run --concurrency=thread -m unittest discover -s ../src/mssql/requests/tests
>>>>>>> 279f4b4c01cb6d4497b29b29eda4f46af2de8a1d

coverage report -m