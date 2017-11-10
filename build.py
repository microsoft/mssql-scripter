#!/usr/bin/env python

# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from __future__ import print_function
from azure.storage.blob import BlockBlobService, ContentSettings
import os
import sys
import utility
import mssqlscripter.mssqltoolsservice.download as mssqltoolsservice

AZURE_STORAGE_CONNECTION_STRING = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
BLOB_CONTAINER_NAME = 'simple'
UPLOADED_PACKAGE_LINKS = []


def print_heading(heading, f=None):
    print('{0}\n{1}\n{0}'.format('=' * len(heading), heading), file=f)


def build(platforms):
    """
        Builds mssql-scripter package.
    """
    print_heading('Cleanup')

    # clean
    utility.clean_up(utility.MSSQLSCRIPTER_DIST_DIRECTORY)
    utility.cleaun_up_egg_info_sub_directories(utility.ROOT_DIR)

    print_heading('Running setup')

    # install general requirements.
    utility.exec_command('pip install -r dev_requirements.txt', utility.ROOT_DIR)

    # convert windows line endings to unix for mssql-cli bash script
    utility.exec_command('python dos2unix.py mssql-scripter mssql-scripter', utility.ROOT_DIR)

    for platform in platforms:
        print_heading('Downloading mssqltoolsservice for platform: {}'.format(platform))
        mssqltoolsservice.download_mssqltoolsservice(platform)

        print_heading('Building mssql-scripter {} wheel package package'.format(platform))
        utility.exec_command('python --version', utility.ROOT_DIR)
        utility.exec_command(
            'python setup.py check -r -s bdist_wheel --plat-name {}'.format(platform), 
            utility.ROOT_DIR,
            continue_on_error=False)
        
        mssqltoolsservice.clean_up_sqltoolsservice()

def _upload_index_file(service, blob_name, title, links):
    print('Uploading index file {}'.format(blob_name))
    service.create_blob_from_text(
        container_name=BLOB_CONTAINER_NAME,
        blob_name=blob_name,
        text="<html><head><title>{0}</title></head><body><h1>{0}</h1>{1}</body></html>"
            .format(title, '\n'.join(
                ['<a href="{0}">{0}</a><br/>'.format(link) for link in links])),
        content_settings=ContentSettings(
            content_type='text/html',
            content_disposition=None,
            content_encoding=None,
            content_language=None,
            content_md5=None,
            cache_control=None
            )
    )


def _gen_pkg_index_html(service, pkg_name):
    links = []
    index_file_name = pkg_name+'/'
    for blob in list(service.list_blobs(BLOB_CONTAINER_NAME, prefix=index_file_name)):
        if blob.name == index_file_name:
            # Exclude the index file from being added to the list
            continue
        links.append(blob.name.replace(index_file_name, ''))
    _upload_index_file(service, index_file_name, 'Links for {}'.format(pkg_name), links)
    UPLOADED_PACKAGE_LINKS.append(index_file_name)


def _upload_package(service, file_path, pkg_name):
    print('Uploading {}'.format(file_path))
    file_name = os.path.basename(file_path)
    blob_name = '{}/{}'.format(pkg_name, file_name)
    service.create_blob_from_path(
        container_name=BLOB_CONTAINER_NAME,
        blob_name=blob_name,
        file_path=file_path
    )
    _gen_pkg_index_html(service, pkg_name)


def validate_package(platforms):
    """
        Install mssql-scripter wheel package locally.
    """
    root_dir = os.path.abspath(os.path.join(os.path.abspath(__file__), '..'))
    # Local install of mssql-scripter.
    mssqlscripter_wheel_dir = os.listdir(utility.MSSQLSCRIPTER_DIST_DIRECTORY)
    current_platform = utility.get_current_platform()

    mssqlscripter_wheel_name = [pkge for pkge in mssqlscripter_wheel_dir if current_platform in pkge]
    print(mssqlscripter_wheel_name)
    # To ensure we have a clean install, we disable the cache as to prevent cache overshadowing actual changes made.
    tility.exec_command(
       'pip install --no-cache-dir --no-index ./dist/{}'.format(mssqlscripter_sdist_name),
       root_dir, continue_on_error=False
    


def publish_daily(platforms):
    """
    Publish mssql-scripter wheel package to daily storage account.
    """
    print('Publishing to simple container within storage account.')
    assert AZURE_STORAGE_CONNECTION_STRING, 'Set AZURE_STORAGE_CONNECTION_STRING environment variable'

    blob_service = BlockBlobService(connection_string=AZURE_STORAGE_CONNECTION_STRING)

    print_heading('Uploading packages to blob storage ')
    for pkg in os.listdir(utility.MSSQLSCRIPTER_DIST_DIRECTORY):
        pkg_path = os.path.join(utility.MSSQLSCRIPTER_DIST_DIRECTORY, pkg)
        print('Uploading package {}'.format(pkg_path))
        _upload_package(blob_service, pkg_path, 'mssql-scripter')
    # Upload the final index file
    _upload_index_file(blob_service, 'index.html', 'Simple Index', UPLOADED_PACKAGE_LINKS)


def publish_official(platforms):
    """
    Publish mssql-scripter wheel package to PyPi.
    """
    mssqlscripter_wheel_dir = os.listdir(utility.MSSQLSCRIPTER_DIST_DIRECTORY)
    # Run twine action for mssqlscripter.
    # Only authorized users with credentials will be able to upload this package.
    # Credentials will be stored in a .pypirc file.
    for mssqlscripter_wheel_name in mssqlscripter_wheel_dir:
        utility.exec_command(
            'twine upload {} pypi'.format(mssqlscripter_wheel_name),
            utility.MSSQLSCRIPTER_DIST_DIRECTORY)


if __name__ == '__main__':
    action = ['build']
    platforms = ['win32', 'win64', 'macosx_10_11_intel', 'manylinux1']

    targets = {
        'build': build,
        'validate_package': validate_package,
        'publish_daily': publish_daily,
        'publish_official': publish_official
    }

    if len(sys.argv) > 1:
        action = sys.argv[1]
    
    if len(sys.argv) > 2:
        platforms = [sys.argv[2]]
    
    if action in targets:
        targets[action](platforms)
    else:
        print('{} is not a supported action'.format(action))
        print('Supported actions are {}'.format(list(targets.keys())))
