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


DOWNLOAD_URL_BASE = 'https://mssqlscripter.blob.core.windows.net/sqltoolsservice-05-24-2017/'

# Supported platform key's must match those in mssqlscript's setup.py.
SUPPORTED_PLATFORMS = {
    'CentOS_7': DOWNLOAD_URL_BASE + 'microsoft.sqltools.servicelayer-centos-x64-netcoreapp1.0.tar.gz',
    'Debian_8': DOWNLOAD_URL_BASE + 'microsoft.sqltools.servicelayer-debian-x64-netcoreapp1.0.tar.gz',
    'Fedora_23': DOWNLOAD_URL_BASE + 'microsoft.sqltools.servicelayer-fedora-x64-netcoreapp1.0.tar.gz',
    'openSUSE_13_2': DOWNLOAD_URL_BASE + 'microsoft.sqltools.servicelayer-opensuse-x64-netcoreapp1.0.tar.gz',
    'OSX_10_11_64': DOWNLOAD_URL_BASE + 'microsoft.sqltools.servicelayer-osx-x64-netcoreapp1.0.tar.gz',
    'RHEL_7': DOWNLOAD_URL_BASE + 'microsoft.sqltools.servicelayer-rhel-x64-netcoreapp1.0.tar.gz',
    'Ubuntu_14': DOWNLOAD_URL_BASE + 'microsoft.sqltools.servicelayer-ubuntu14-x64-netcoreapp1.0.tar.gz',
    'Ubuntu_16': DOWNLOAD_URL_BASE + 'microsoft.sqltools.servicelayer-ubuntu16-x64-netcoreapp1.0.tar.gz',
    'Windows_7_64': DOWNLOAD_URL_BASE + 'microsoft.sqltools.servicelayer-win-x64-netcoreapp1.0.zip',
    'Windows_7_86': DOWNLOAD_URL_BASE + 'microsoft.sqltools.servicelayer-win-x86-netcoreapp1.0.zip',
}

CURRENT_DIRECTORY = os.path.abspath(os.path.join(os.path.abspath(__file__), '..'))
BUILD_DIRECTORY = os.path.abspath(os.path.join(CURRENT_DIRECTORY, 'build'))
TARGET_DIRECTORY = os.path.abspath(os.path.join(os.path.abspath(__file__), '..', 'mssqltoolsservice', 'bin'))


def download_and_unzip(download_file_path, directory):
    """
        Download and unzip files to the target directory.
    """
    # Download and unzip each file.
    if download_file_path.endswith('tar.gz'):
        response = urlopen(download_file_path)
        compressed_file = tarfile.open(mode='r|gz', fileobj=response)
    elif download_file_path.endswith('.zip'):
        response = response = requests.get(download_file_path)
        compressed_file = zipfile.ZipFile(io.BytesIO(response.content))

    if not os.path.exists(directory):
        os.makedirs(directory)

    print(u'Extracting files from {}'.format(download_file_path))
    compressed_file.extractall(directory)


def build_sqltoolsservice_wheels(platforms):
    """
        For each supported platform, build a universal wheel.
    """
    # Clean up dangling directories if previous run was interrupted.
    utility.clean_up(directory=TARGET_DIRECTORY)
    utility.clean_up(directory=BUILD_DIRECTORY)

    if not platforms:
            # Defaults to all supported platforms.
        platforms = SUPPORTED_PLATFORMS.keys()

    print(u'Generating .whl files for the following platforms: {}'.format(platforms))
    for platform in platforms:
        if platform not in SUPPORTED_PLATFORMS:
            print(u'{} is not a supported platform'.format(platform))
            break
        # Set environment variable to communicate current platform to setup.py.
        os.environ[u'MSSQLTOOLSSERVICE_PLATFORM'] = platform

        print(u'Calling setup bdist_wheel for platform:{}'.format(platform))
        download_and_unzip(SUPPORTED_PLATFORMS[platform], directory=TARGET_DIRECTORY)
        utility.exec_command(u'python setup.py check -r -s bdist_wheel', CURRENT_DIRECTORY)

        print(u'Cleaning up mssqltoolservice and build directory for platform:{}'.format(platform))
        utility.clean_up(directory=TARGET_DIRECTORY)
        utility.clean_up(directory=BUILD_DIRECTORY)


if __name__ == '__main__':
    build_sqltoolsservice_wheels(sys.argv[1:])
