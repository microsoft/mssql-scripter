#!/usr/bin/env python

# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import io
import os
import platform as _platform
import site
import sys
import tarfile
import zipfile

from setuptools import setup
from setuptools.command.install import install

VERSION = "0.1.1.dev"

DOWNLOAD_URL_BASE = 'https://mssqlscripter.blob.core.windows.net/sqltoolsservice-04-07-2017/'


PLATFORM_FILE_NAMES = {
    'CentOS_7 ': DOWNLOAD_URL_BASE + 'microsoft.sqltools.servicelayer-centos-x64-netcoreapp1.0.tar.gz',
    'DEBIAN_8': DOWNLOAD_URL_BASE + 'microsoft.sqltools.servicelayer-debian-x64-netcoreapp1.0.tar.gz',
    'Fedora_23': DOWNLOAD_URL_BASE + 'microsoft.sqltools.servicelayer-fedora-x64-netcoreapp1.0.tar.gz',
    'openSUSE_13_2': DOWNLOAD_URL_BASE + 'microsoft.sqltools.servicelayer-opensuse-x64-netcoreapp1.0.tar.gz',
    'OSX_10_11_64': DOWNLOAD_URL_BASE + 'microsoft.sqltools.servicelayer-osx-x64-netcoreapp1.0.tar.gz',
    'RHEL_7': DOWNLOAD_URL_BASE + 'microsoft.sqltools.servicelayer-rhel-x64-netcoreapp1.0.tar.gz',
    'Ubuntu_14': DOWNLOAD_URL_BASE + 'microsoft.sqltools.servicelayer-ubuntu14-x64-netcoreapp1.0.tar.gz',
    'Ubuntu_16': DOWNLOAD_URL_BASE + 'microsoft.sqltools.servicelayer-ubuntu16-x64-netcoreapp1.0.tar.gz',
    'Windows_7_64': DOWNLOAD_URL_BASE + 'microsoft.sqltools.servicelayer-win-x64-netcoreapp1.0.zip',
    'Windows_7_86': DOWNLOAD_URL_BASE + 'microsoft.sqltools.servicelayer-win-x86-netcoreapp1.0.zip',
}

LINUX_DISTRO_NO_VERSION = {
    'centos': 'CentOS_7',
    'ol': 'CentOS_7',
    'fedora': 'Fedora_23',
    'opensuse': 'OpenSUSE_13_2',
    'rhel': 'RHEL_7',
    'debian': 'Debian_8',
}

LINUX_DISTRO_WITH_VERSION = {
    'ubuntu':
        {
            '14': 'Ubuntu_14',
            '16': 'Ubuntu_16'
        },
    'elementary':
        {
            '0.3': 'Ubuntu_14',
            '0.4': 'Ubuntu_16'
        },
    'elementaryOS':
        {
            '0.3': 'Ubuntu_14',
            '0.4': 'Ubuntu_16'
        },
    'linuxmint':
        {
            '18': 'Ubuntu_16'
        },
    'galliumos':
        {
            '2.0': 'Ubuntu_16'
        },
}
try:
    # Find site-packages for current user.
    site_packages_dir = site.getusersitepackages()
except AttributeError:
    # When we are in a virtual environment, there is no distinction between a user or sys account as 
    # there is only one site-packages for the python of that environment. 
    # What we do is find where pip is installed in the virtual environment and install ourselves there.
    import pip
    site_packages_dir = os.path.abspath(os.path.join(
        os.path.abspath(pip.__file__),
        '..',
        '..'))

TOOLS_SERVICE_TARGET_DIR = os.path.join(
    site_packages_dir, 'mssqlscripter', 'sqltoolsservice')


def _get_runtime_id(
        system=_platform.system(),
        architecture=_platform.architecture()[0],
        version=_platform.version()):
    """
        Find supported run time id for current platform.
    """
    run_time_id = None

    if (system == 'Windows'):
        if (architecture == '32bit'):
            run_time_id = 'Windows_7_86'
        elif (architecture == '64bit'):
            run_time_id = 'Windows_7_64'
    elif (system == 'Darwin'):
        if (architecture == '64bit'):
            run_time_id = 'OSX_10_11_64'
    elif (system == 'Linux'):
        if (architecture == '64bit'):
            run_time_id = get_linux_distro_runtime_id()

    return run_time_id


def get_download_url(run_time_id=_get_runtime_id()):
    """
        Retrieve sql tools service download link on a supported run time id.
    """
    if run_time_id and run_time_id in PLATFORM_FILE_NAMES:
        return PLATFORM_FILE_NAMES[run_time_id]


def install_sql_tools_service(download_file_path, target_directory=TOOLS_SERVICE_TARGET_DIR):
    """
        Installs native sql tools service to either site-packages/mssql/sqltoolsservice or custom directory.
    """
    import requests
    from future.standard_library import install_aliases
    install_aliases()
    from urllib.request import urlopen

    if download_file_path.endswith('tar.gz'):
        response = urlopen(download_file_path)
        compressed_file = tarfile.open(mode='r|gz', fileobj=response)
    elif download_file_path.endswith('.zip'):
        response = response = requests.get(download_file_path)
        compressed_file = zipfile.ZipFile(io.BytesIO(response.content))

    if not os.path.exists(target_directory):
        os.makedirs(target_directory)

    compressed_file.extractall(target_directory)


def _get_linux_distro_from_file(non_default_file=None):
    """
        Find linux distro based on
        https://www.freedesktop.org/software/systemd/man/os-release.html.
    """
    os_release_info_file = None

    if os.path.exists(non_default_file):
        os_release_info_file = non_default_file
    elif os.path.exists('/etc/os-release'):
        os_release_info_file = '/etc/os-release'
    elif os.path.exists('/usr/lib/os-release'):
        os_release_info_file = '/usr/lib/os-release'

    with open(os_release_info_file, 'r', encoding='utf-8') as os_release_file:
        content = os_release_file.read()
        return get_linux_distro_runtime_id(content)


def _get_linux_distro_runtime_id(content):
    """
        Parse content for linux distro run time id.
     """
    name = None
    version = None
    id_like = None

    # Try to find name, version and id_like best effort.
    for line in content.splitlines():
        key, value = line.rstrip().split('=')
        value = value.strip('"')
        if key == 'ID':
            name = value
        elif key == 'VERSION_ID':
            version = value
        elif key == 'ID_LIKE':
            id_like = value.split(' ')
        if name and version and id_like:
            break
    # First try the distribution name.
    run_time_id = _get_runtime_id_helper(name, version)

    # If we don't understand it, try the 'ID_LIKE' field.
    if not run_time_id and id_like:
        for name in id_like:
            run_time_id = _get_runtime_id_helper(name, version)
            if run_time_id:
                break

    return run_time_id


def _get_runtime_id_helper(name, version):
    """
        Checks if linux distro name and version match to a supported package.
    """
    if name in LINUX_DISTRO_NO_VERSION:
        return LINUX_DISTRO_NO_VERSION[name]

    if name in LINUX_DISTRO_WITH_VERSION:
        for supported_version in LINUX_DISTRO_WITH_VERSION[name]:
            if version.startswith(supported_version):
                return LINUX_DISTRO_WITH_VERSION[name][supported_version]
    return None
    
class Install_Native_Dependencies(install):
    """
        Downloads and Installs native sql tools service if platform is supported.
    """

    def run(self):

        sqltoolsservice_url = get_download_url()

        # Only install if sql tools service is supported.
        if sqltoolsservice_url:
            # We only install if sql tools service is supported on this platform.
            # Install sql tools service only if the install was successful; this prevents a dangling sqltoolsservice folder
            # when mssql-scripter was not installed succesfully.
            install.run(self)
            install_sql_tools_service(sqltoolsservice_url)
            return

        raise EnvironmentError('Installation unsuccesful: Sql Tools service is not supported on this platform.')

CLASSIFIERS = [
    'Development Status :: 2 - Pre-Alpha',
    'Intended Audience :: Developers',
    'Intended Audience :: System Administrators',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'License :: OSI Approved :: MIT License',
]

DEPENDENCIES = [
    'pip',
    'future',
    'site'
]

SETUP_DEPENDENCIES = [
    'requests',
    'future'
]

if sys.version_info < (3, 4):
    DEPENDENCIES.append('enum34')

setup(
    setup_requires=SETUP_DEPENDENCIES,
    install_requires=DEPENDENCIES,
    name='mssql-scripter',
    version=VERSION,
    description='Microsoft SQL Scripter Command-Line Tool',
    license='MIT',
    author='Microsoft Corporation',
    author_email='sqlxplatclieng@microsoft.com',
    url='https://github.com/Microsoft/sql-xplat-cli/',
    zip_safe=True,
    classifiers=CLASSIFIERS,
    include_package_data=True,
    scripts=[
        'mssql-scripter',
        'mssql-scripter.bat'
    ],
    packages=[
        'mssqlscripter',
        'mssqlscripter.jsonrpc',
        'mssqlscripter.jsonrpc.contracts'],
    dependency_links=['/Users/beeboop/Documents/sql-xplat-cli/sqltoolsservicesetup/sqltoolsservice_macosx2.egg-info']
    cmdclass={'install': Install_Native_Dependencies},
)
