# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
from __future__ import print_function

import io
import os
import requests
import sys
import tarfile
import utility
import zipfile

from future.standard_library import install_aliases
install_aliases()
from urllib.request import urlopen



DOWNLOAD_URL_BASE = 'https://mssqlscripter.blob.core.windows.net/sqltoolsservice-10-12-2017/'

# Supported platform key's must match those in mssqlscript's setup.py.
SUPPORTED_PLATFORMS = {
    'manylinux1': DOWNLOAD_URL_BASE + 'Microsoft.SqlTools.ServiceLayer-linux-x64-netcoreapp2.0.tar.gz',
    'macosx_10_11_intel': DOWNLOAD_URL_BASE + 'Microsoft.SqlTools.ServiceLayer-osx-x64-netcoreapp2.0.tar.gz',
    'win64': DOWNLOAD_URL_BASE + 'Microsoft.SqlTools.ServiceLayer-win-x64-netcoreapp2.0.zip',
    'win32': DOWNLOAD_URL_BASE + 'Microsoft.SqlTools.ServiceLayer-win-x86-netcoreapp2.0.zip'
}

TARGET_DIRECTORY = os.path.abspath(os.path.join(os.path.abspath(__file__), '..', 'bin'))

def download_mssqltoolsservice(platform):
    """
        For each supported platform, build a universal wheel.
    """
    # Clean up dangling directories if previous run was interrupted.
    utility.clean_up(directory=TARGET_DIRECTORY)

    if not platform or platform not in SUPPORTED_PLATFORMS:
        print('Please provide a valid platform flag. [win32, win64, manylinux1, macosx_10_11_intel]')
        return 

    download_file_path = SUPPORTED_PLATFORMS[platform]

    if download_file_path.endswith('tar.gz'):
        response = urlopen(download_file_path)
        compressed_file = tarfile.open(mode='r|gz', fileobj=response)
    elif download_file_path.endswith('.zip'):
        response = response = requests.get(download_file_path)
        compressed_file = zipfile.ZipFile(io.BytesIO(response.content))

    if not os.path.exists(TARGET_DIRECTORY):
        os.makedirs(TARGET_DIRECTORY)
    
    print(u'Downloading mssqltoolsservice for this platform.')
    print(u'Extracting files from {}'.format(download_file_path))
    compressed_file.extractall(TARGET_DIRECTORY)


def clean_up_sqltoolsservice():
    utility.clean_up(directory=TARGET_DIRECTORY)

