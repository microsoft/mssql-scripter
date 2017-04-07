# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import io
import os
import platform as _platform
import site
import tarfile
import zipfile


DOWNLOAD_URL_BASE = 'https://mssqlscripter.blob.core.windows.net/sqltoolservice-03-31-2017/'

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
    for path in site.getsitepackages():
        if (path.endswith('site-packages')):
            site_packages_dir = path
            break
except AttributeError:
    # getsitepackages() does not work in virtual environment for python 2.
    # TODO: Add support for production use in a virtual env.
    pass

TOOLS_SERVICE_TARGET_DIR = os.path.join(site_packages_dir, 'mssql', 'sqltoolsservice')

def _get_runtime_id(
        system=_platform.system(),
        architecture=_platform.architecture()[0],
        version=_platform.version()):
    """
        Finds the run time id of current platform if supported.
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
        # TODO: Not sure if this will be the string for linux distro
        if (architecture == '64bit'):
            run_time_id = get_linux_distro_runtime_id()

    return run_time_id

def get_download_url(run_time_id=_get_runtime_id()):
    """
        Retrieves the download link on a supported run time id.
    """
    if (run_time_id and run_time_id in PLATFORM_FILE_NAMES):
        return PLATFORM_FILE_NAMES[run_time_id]

def install(download_file_path, target_directory=TOOLS_SERVICE_TARGET_DIR):
    """
        Installs native sql tools service to either site-packages/mssql/sqltoolsservice or custom directory.
    """

    # TODO: Refactor, there has to be a way to submit a single request against any file and extract them.
    # TODO: Revisit for case where request fails.
    import requests
    from future.standard_library import install_aliases
    install_aliases()
    from urllib.request import urlopen

    if (download_file_path.endswith('tar.gz')):
        response = urlopen(download_file_path)
        compressed_file = tarfile.open(mode='r|gz', fileobj=response)
    elif (download_file_path.endswith('.zip')):
        response = response = requests.get(download_file_path)
        compressed_file = zipfile.ZipFile(io.BytesIO(response.content))

    if (not os.path.exists(target_directory)):
        os.makedirs(target_directory)

    compressed_file.extractall(target_directory)



def _get_linux_distro_from_file(non_default_file=None):
    """
        Find linux distro based on
        https://www.freedesktop.org/software/systemd/man/os-release.html.
    """
    os_release_info_file = None

    if(os.path.exists(non_default_file)):
        os_release_info_file = non_default_file
    elif (os.path.exists('/etc/os-release')):
        os_release_info_file = '/etc/os-release'
    elif (os.path.exists('/usr/lib/os-release')):
        os_release_info_file = '/usr/lib/os-release'

    with open(os_release_info_file, 'r', encoding='utf-8') as os_release_file:
        content = os_release_file.read()
        return get_linux_distro_runtime_id(content)

def _get_linux_distro_runtime_id(content):
    """
        Will parse content for linux distro run time id.
     """

    name = None
    version = None
    id_like = None

    # Try to find name, version and id_like best effort
    for line in content.splitlines():
        key, value = line.rstrip().split('=')
        value = value.strip('"')
        if (key == 'ID'):
            name = value
        elif (key == 'VERSION_ID'):
            version = value
        elif (key == 'ID_LIKE'):
            id_like = value.split(' ')
        if (name and version and id_like):
            break
    # First try the distribution name
    run_time_id = _get_runtime_id_helper(name, version)

    # If we don't understand it, try the 'ID_LIKE' field
    if (run_time_id is None and id_like):
        for name in id_like:
            run_time_id = _get_runtime_id_helper(name, version)
            if (run_time_id):
                break

    return run_time_id


def _get_runtime_id_helper(name, version):
    """
        Checks if linux distro name and version match to a supported package.
    """
    if (name in LINUX_DISTRO_NO_VERSION):
        return LINUX_DISTRO_NO_VERSION[name]

    if (name in LINUX_DISTRO_WITH_VERSION):
        for supported_version in LINUX_DISTRO_WITH_VERSION[name]:
            if (version.startswith(supported_version)):
                return LINUX_DISTRO_WITH_VERSION[name][supported_version]
    return None
