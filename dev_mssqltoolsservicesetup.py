# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import os
import platform as _platform

# mssqltoolsservice version should be kept in sync with mssqlscripter.
MSSQLTOOLSSERVICE_VERSION = "0.1.1.dev0"
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

def get_mssqltoolsservice_if_supported(run_time_id=_get_runtime_id()):
    """
        Retrieve sql tools service package name for this platform if supported.
    """
    if run_time_id and run_time_id in MSSQLTOOLSSERVICE_PACKAGE_SUFFIX:
        return MSSQLTOOLSSERVICE_PACKAGE_NAME.format(run_time_id, MSSQLTOOLSSERVICE_VERSION)

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
        return _get_linux_distro_runtime_id(content)


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
    