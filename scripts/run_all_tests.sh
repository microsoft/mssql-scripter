#!/usr/bin/env bash
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

python -m unittest discover -s ../src/common/tests
python -m unittest discover -s ../src/mssql/scripter/tests
