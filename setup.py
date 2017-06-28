#!/usr/bin/env python

# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import io
import os
import platform as _platform
import sys

from setuptools import setup

# This version number is in place in two places and must be in sync with
# mssqltoolsservice's version in setup.py.
MSSQLSCRIPTER_VERSION = '1.0.0a15'

# If we have the source, validate our setup version matches source version.
# This will prevent uploading releases with mismatched versions. This will
# also ensure mssqlscripter's version is in sync with mssqltoolsservice.
try:
    with io.open('mssqlscripter/__init__.py', 'r', encoding='utf-8') as f:
        mssqlscripter_info = f.read()
    with io.open('mssqltoolsservice/mssqltoolsservice/__init__.py', 'r', encoding='utf-8') as f:
        mssqltoolsservice_info = f.read()
except IOError:
    pass
else:
    import re
    # Use regex to parse for version.
    scripter_version = re.search(
        r'__version__\s*=\s*[\'"](.+?)[\'"]',
        mssqlscripter_info)
    toolsservice_version = re.search(
        r'__version__\s*=\s*[\'"](.+?)[\'"]',
        mssqltoolsservice_info)

    if not scripter_version:
        print('Could not find __version__ in mssqlscripter/__init__.py')
        sys.exit(1)
    if not toolsservice_version:
        print(
            'Could not find __version__ in mssqltoolsservice/mssqltoolsservice/__init__.py')
        sys.exit(1)
    # Validate mssqlscripter source and setup versions.
    if scripter_version.group(1) != MSSQLSCRIPTER_VERSION:
        print('mssqlscripter version mismatch, source = "{}"; setup = "{}"'.format(
            scripter_version.group(1), MSSQLSCRIPTER_VERSION))
        sys.exit(1)
    # Validate mssqlscripter version with mssqltoolsservice.
    if scripter_version.group(1) != toolsservice_version.group(1):
        print(
            'mssqltoolsservice version mismatch, mssqscripter = "{}"; mssqltoolsservice = "{}"'.format(
                scripter_version.group(1),
                toolsservice_version.group(1)))
        sys.exit(1)

MSSQLTOOLSSERVICE_PACKAGE_NAME = 'mssqltoolsservice_{}=={}'
MSSQLTOOLSSERVICE_PACKAGE_SUFFIX = [
    'CentOS_7',
    'Debian_8',
    'Fedora_23',
    'openSUSE_13_2',
    'OSX_10_11_64',
    'RHEL_7',
    'Ubuntu_14',
    'Ubuntu_16',
    'Windows_7_64',
    'Windows_7_86'
]

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


def _get_linux_distro_from_file():
    """
        Find linux distro based on
        https://www.freedesktop.org/software/systemd/man/os-release.html.
    """
    os_release_info_file = None

    if os.path.exists('/etc/os-release'):
        os_release_info_file = '/etc/os-release'
    elif os.path.exists('/usr/lib/os-release'):
        os_release_info_file = '/usr/lib/os-release'
    else:
        raise EnvironmentError('Error detecting Linux distro version.')

    with io.open(os_release_info_file, 'r', encoding='utf-8') as os_release_file:
        content = os_release_file.read()
        return _get_linux_distro_runtime_id(content)


def _get_runtime_id(
        system=_platform.system(),
        architecture=_platform.architecture()[0],
        version=_platform.version()):
    """
        Find supported run time id for current platform.
    """
    run_time_id = None

    if system == 'Windows':
        if architecture == '32bit':
            run_time_id = 'Windows_7_86'
        elif architecture == '64bit':
            run_time_id = 'Windows_7_64'
    elif system == 'Darwin':
        if architecture == '64bit':
            run_time_id = 'OSX_10_11_64'
    elif system == 'Linux':
        if architecture == '64bit':
            run_time_id = _get_linux_distro_from_file()

    return run_time_id


def get_mssqltoolsservice_package_name(run_time_id=_get_runtime_id()):
    """
        Retrieve sql tools service package name for this platform if supported.
    """
    if run_time_id and run_time_id in MSSQLTOOLSSERVICE_PACKAGE_SUFFIX:
        # set package suffix name for other uses like building wheels outside of setup.py.
        os.environ['MSSQLTOOLSSERVICE_PACKAGE_SUFFIX'] = run_time_id
        return MSSQLTOOLSSERVICE_PACKAGE_NAME.format(
            run_time_id, MSSQLSCRIPTER_VERSION)

    raise EnvironmentError('mssqltoolsservice is not supported on this platform.')


CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Intended Audience :: System Administrators',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'License :: OSI Approved :: MIT License',
]

DEPENDENCIES = [
    'future>=0.16.0',
    'wheel>=0.29.0'
]

if sys.version_info < (3, 4):
    DEPENDENCIES.append('enum34>=1.1.6')

DEPENDENCIES.append(get_mssqltoolsservice_package_name())

# Using a environment variable to communicate mssqltoolsservice package name for
# other modules that need that info like dev_setup.py.
os.environ['MSSQLTOOLSSERVICE_PACKAGE_NAME'] = DEPENDENCIES[-1]

setup(
    install_requires=DEPENDENCIES,
    name='mssql-scripter',
    version=MSSQLSCRIPTER_VERSION,
    description='Microsoft SQL Scripter Command-Line Tool',
    license='MIT',
    author='Microsoft Corporation',
    author_email='sqlxplatclieng@microsoft.com',
    url='https://github.com/Microsoft/sql-xplat-cli/',
    zip_safe=True,
    long_description=open('README.rst').read(),
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
)
