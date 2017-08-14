#!/usr/bin/env python

# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from __future__ import print_function
import os
import re
import sys
import tempfile
import utility
from azure.storage.blob import BlockBlobService, ContentSettings

BLOB_SERVICE_CONNECTION_STRING = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
BLOB_CONTAINER_NAME = 'simple'
UPLOADED_PACKAGE_LINKS = [] 


def print_heading(heading, f=None):
    print('{0}\n{1}\n{0}'.format('=' * len(heading), heading), file=f)


def upload_index_file(service, blob_name, title, links):
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


def gen_pkg_index_html(service, pkg_name):
    links = []
    index_file_name = pkg_name+'/'
    for blob in list(service.list_blobs(BLOB_CONTAINER_NAME, prefix=index_file_name)):
        if blob.name == index_file_name:
            # Exclude the index file from being added to the list
            continue
        links.append(blob.name.replace(index_file_name, ''))
    upload_index_file(service, index_file_name, 'Links for {}'.format(pkg_name), links)
    UPLOADED_PACKAGE_LINKS.append(index_file_name)


def upload_package(service, file_path, pkg_name):
    print('Uploading {}'.format(file_path))
    file_name = os.path.basename(file_path)
    blob_name = '{}/{}'.format(pkg_name, file_name)
    service.create_blob_from_path(
        container_name=BLOB_CONTAINER_NAME,
        blob_name=blob_name,
        file_path=file_path
    )
    gen_pkg_index_html(service, pkg_name)


def build(options):

    supported_actions = ['nightly']
    action = None

    if len(options) >= 1:
        if options[0] not in supported_actions:
            print('Please provide a supported action {}.'.format(supported_actions))
            return
        action = options[0]


    print_heading('Cleanup')

    # clean
    utility.clean_up(utility.MSSQLSCRIPTER_DIST_DIRECTORY)
    utility.clean_up(utility.MSSQLTOOLSSERVICE_DIST_DIRECTORY)
    utility.cleaun_up_egg_info_sub_directories(utility.ROOT_DIR)
    utility.cleaun_up_egg_info_sub_directories(utility.MSSQLTOOLSSERVICE_DIRECTORY)
    
    print_heading('Running setup')
    
    # install general requirements.
    utility.exec_command('pip install -r dev_requirements.txt', utility.ROOT_DIR)
    
    print_heading('Running mssql-scripter tests')
    utility.exec_command('tox', utility.ROOT_DIR, continue_on_error = False)
    
    print_heading('Building mssql-scripter pip package')
    utility.exec_command('python setup.py check -r -s sdist', utility.ROOT_DIR, continue_on_error = False)
    
    print_heading('Building mssqltoolsservice pip package')
    utility.exec_command('python buildwheels.py', utility.MSSQLTOOLSSERVICE_DIRECTORY, continue_on_error = False)

    if action == 'nightly':
        assert BLOB_SERVICE_CONNECTION_STRING, 'Set AZURE_STORAGE_CONNECTION_STRING environment variable'
        blob_service = BlockBlobService(connection_string=BLOB_SERVICE_CONNECTION_STRING)
    
        print_heading('Uploading packages to blob storage ')
        for pkg in os.listdir(utility.MSSQLSCRIPTER_DIST_DIRECTORY):
            pkg_path = os.path.join(utility.MSSQLSCRIPTER_DIST_DIRECTORY, pkg)
            print('Uploading package {}'.format(pkg_path))
            upload_package(blob_service, pkg_path, 'mssql-scripter')
    
        for pkg in os.listdir(utility.MSSQLTOOLSSERVICE_DIST_DIRECTORY):
            pkg_path = os.path.join(utility.MSSQLTOOLSSERVICE_DIST_DIRECTORY, pkg)
            pkg_name = os.path.basename(pkg_path).split('-')[0].replace('_', '-').lower()
            print('Uploading package {}'.format(pkg_name))
            upload_package(blob_service, pkg_path, pkg_name)

        # Upload the final index file
        upload_index_file(blob_service, 'index.html', 'Simple Index', UPLOADED_PACKAGE_LINKS)


if __name__ == '__main__':
    build(sys.argv[1:])