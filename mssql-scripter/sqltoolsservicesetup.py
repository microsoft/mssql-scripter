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


DOWNLOAD_URL_BASE = u'https://mssqlscripter.blob.core.windows.net/sqltoolservice-03-31-2017/'

PLATFORM_FILE_NAMES = {
    u'CentOS_7 ': DOWNLOAD_URL_BASE + u'microsoft.sqltools.servicelayer-centos-x64-netcoreapp1.0.tar.gz',
    u'DEBIAN_8': DOWNLOAD_URL_BASE + u'microsoft.sqltools.servicelayer-debian-x64-netcoreapp1.0.tar.gz',
    u'Fedora_23': DOWNLOAD_URL_BASE + u'microsoft.sqltools.servicelayer-fedora-x64-netcoreapp1.0.tar.gz',
    u'openSUSE_13_2': DOWNLOAD_URL_BASE + u'microsoft.sqltools.servicelayer-opensuse-x64-netcoreapp1.0.tar.gz',
    u'OSX_10_11_64': DOWNLOAD_URL_BASE + u'microsoft.sqltools.servicelayer-osx-x64-netcoreapp1.0.tar.gz',
    u'RHEL_7': DOWNLOAD_URL_BASE + u'microsoft.sqltools.servicelayer-rhel-x64-netcoreapp1.0.tar.gz',
    u'Ubuntu_14': DOWNLOAD_URL_BASE + u'microsoft.sqltools.servicelayer-ubuntu14-x64-netcoreapp1.0.tar.gz',
    u'Ubuntu_16': DOWNLOAD_URL_BASE + u'microsoft.sqltools.servicelayer-ubuntu16-x64-netcoreapp1.0.tar.gz',
    u'Windows_7_64': DOWNLOAD_URL_BASE + u'microsoft.sqltools.servicelayer-win-x64-netcoreapp1.0.zip',
    u'Windows_7_86': DOWNLOAD_URL_BASE + u'microsoft.sqltools.servicelayer-win-x86-netcoreapp1.0.zip',
}

LINUX_DISTRO_NO_VERSION = {
    u'centos': u'CentOS_7',
    u'ol': u'CentOS_7',
    u'fedora': u'Fedora_23',
    u'opensuse': u'OpenSUSE_13_2',
    u'rhel': u'RHEL_7',
    u'debian': u'Debian_8',
}

LINUX_DISTRO_WITH_VERSION = {
    u'ubuntu':
        {
            u'14': u'Ubuntu_14',
            u'16': u'Ubuntu_16'
        },
    u'elementary':
        {
            u'0.3': u'Ubuntu_14',
            u'0.4': u'Ubuntu_16'
        },
    u'elementaryOS':
        {
            u'0.3': u'Ubuntu_14',
            u'0.4': u'Ubuntu_16'
        },
    u'linuxmint':
        {
            u'18': u'Ubuntu_16'
        },
    u'galliumos':
        {
            u'2.0': u'Ubuntu_16'
        },
}
try:
    for path in site.getsitepackages():
        if path.endswith(u'site-packages'):
            site_packages_dir = path
            break
except AttributeError:
    # getsitepackages() does not work in virtual environment for python 2.
    # TODO: Add support for production use in a virtual env.
    pass


TOOLS_SERVICE_TARGET_DIR = os.path.join(
    site_packages_dir, u'mssql', u'sqltoolsservice')


def _get_runtime_id(
        system=_platform.system(),
        architecture=_platform.architecture()[0],
        version=_platform.version()):
    """
        Find supported run time id for current platform.
    """
    run_time_id = None

    if (system == u'Windows'):
        if (architecture == u'32bit'):
            run_time_id = u'Windows_7_86'
        elif (architecture == u'64bit'):
            run_time_id = u'Windows_7_64'
    elif (system == u'Darwin'):
        if (architecture == u'64bit'):
            run_time_id = u'OSX_10_11_64'
    elif (system == u'Linux'):
        # TODO: Not sure if this will be the string for linux distro.
        if (architecture == u'64bit'):
            run_time_id = get_linux_distro_runtime_id()

    return run_time_id


def get_download_url(run_time_id=_get_runtime_id()):
    """
        Retrieve sql tools service download link on a supported run time id.
    """
    if run_time_id and run_time_id in PLATFORM_FILE_NAMES:
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

    if download_file_path.endswith(u'tar.gz'):
        response = urlopen(download_file_path)
        compressed_file = tarfile.open(mode=u'r|gz', fileobj=response)
    elif download_file_path.endswith(u'.zip'):
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
    elif os.path.exists(u'/etc/os-release'):
        os_release_info_file = u'/etc/os-release'
    elif os.path.exists(u'/usr/lib/os-release'):
        os_release_info_file = u'/usr/lib/os-release'

    with open(os_release_info_file, u'r', encoding=u'utf-8') as os_release_file:
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
        if key == u'ID':
            name = value
        elif key == u'VERSION_ID':
            version = value
        elif key == u'ID_LIKE':
            id_like = value.split(u' ')
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
