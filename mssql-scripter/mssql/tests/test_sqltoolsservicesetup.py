# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import unittest
import sqltoolsservicesetup


class TestSqlToolsServiceSetup(unittest.TestCase):

    def test_native_dependency_download_path(self):
        """
            Verifies correct download link is return based on platform and architecture.
        """
        windows_32_id = sqltoolsservicesetup._get_runtime_id(
            system='Windows', architecture='32bit')
        windows_64_id = sqltoolsservicesetup._get_runtime_id(
            system='Windows', architecture='64bit')
        mac_64_id = sqltoolsservicesetup._get_runtime_id(
            system='Darwin', architecture='64bit')

        self.assertEqual(windows_32_id, 'Windows_7_86')
        self.assertEqual(windows_64_id, 'Windows_7_64')
        self.assertEqual(mac_64_id, 'OSX_10_11_64')

        windows_32_link = sqltoolsservicesetup.get_download_url(windows_32_id) 
        windows_64_link = sqltoolsservicesetup.get_download_url(windows_64_id)
        mac_64_link = sqltoolsservicesetup.get_download_url(mac_64_id)

        self.assertTrue(
            'microsoft.sqltools.servicelayer-win-x86-netcoreapp1.0.zip' in windows_32_link)
        self.assertTrue(
            'microsoft.sqltools.servicelayer-win-x64-netcoreapp1.0.zip' in windows_64_link)
        self.assertTrue(
            'microsoft.sqltools.servicelayer-osx-x64-netcoreapp1.0.tar.gz' in mac_64_link)

    def test_get_linux_distro_runtime_id(self):
        """
            Verifies Linux distro runtime id can be extracted from contents found in /etc/os-release.
        """
        # Copied from /etc/os-release on Ubuntu 14.04.
        distro_ubuntu_14_04 = (
            'NAME="Ubuntu"\n'
            'VERSION="14.04.5 LTS, Trusty Tahr"\n'
            'ID=ubuntu\n'
            'ID_LIKE=debian\n'
            'PRETTY_NAME="Ubuntu 14.04.5 LTS"\n'
            'VERSION_ID="14.04"\n'
            'HOME_URL="http://www.ubuntu.com/"\n'
            'SUPPORT_URL="http://help.ubuntu.com/"\n'
            'BUG_REPORT_URL="http://bugs.launchpad.net/ubuntu/"\n'
        )
        # Copied from /etc/os-release on Fedora 23.
        distro_fedora_23 = (
            'NAME=Fedora\n'
            'VERSION="23 (Workstation Edition)"\n'
            'ID=fedora\n'
            'VERSION_ID=23\n'
            'PRETTY_NAME="Fedora 23 (Workstation Edition)"\n'
            'ANSI_COLOR="0;34"\n'
            'CPE_NAME="cpe:/o:fedoraproject:fedora:23"\n'
            'HOME_URL="https://fedoraproject.org/"\n'
            'BUG_REPORT_URL="https://bugzilla.redhat.com/"\n'
            'REDHAT_BUGZILLA_PRODUCT="Fedora"\n'
            'REDHAT_BUGZILLA_PRODUCT_VERSION=23\n'
            'REDHAT_SUPPORT_PRODUCT="Fedora"\n'
            'REDHAT_SUPPORT_PRODUCT_VERSION=23\n'
            'PRIVACY_POLICY_URL=https://fedoraproject.org/wiki/Legal:PrivacyPolicy\n'
            'VARIANT="Workstation Edition"\n'
            'VARIANT_ID=workstation`\n'
        )

        # Copied from /etc/os-release on Debian 8.
        distro_debian_8 = (
            'PRETTY_NAME="Debian GNU/Linux 8 (jessie)"\n'
            'NAME="Debian GNU/Linux"\n'
            'VERSION_ID="8"\n'
            'VERSION="8 (jessie)"\n'
            'ID=debian\n'
            'HOME_URL="http://www.debian.org/"\n'
            'SUPPORT_URL="http://www.debian.org/support"\n'
            'BUG_REPORT_URL="https://bugs.debian.org/"`;\n'
        )
        # Copied from /etc/os-release on CentOS 7.
        distro_centos_7 = (
            'NAME="CentOS Linux"\n'
            'VERSION="7 (Core)"\n'
            'ID="centos"\n'
            'ID_LIKE="rhel fedora"\n'
            'VERSION_ID="7"\n'
            'PRETTY_NAME="CentOS Linux 7 (Core)"\n'
            'ANSI_COLOR="0;31"\n'
            'CPE_NAME="cpe:/o:centos:centos:7"\n'
            'HOME_URL="https://www.centos.org/"\n'
            'BUG_REPORT_URL="https://bugs.centos.org/"\n'
            'CENTOS_MANTISBT_PROJECT="CentOS-7"\n'
            'CENTOS_MANTISBT_PROJECT_VERSION="7"\n'
            'REDHAT_SUPPORT_PRODUCT="centos"\n'
            'REDHAT_SUPPORT_PRODUCT_VERSION="7"`\n'
        )
        # Copied from /etc/os-release on KDE Neon 5.8.
        distro_kde_neon_5_8 = (
            'NAME="KDE neon"\n'
            'VERSION="5.8"\n'
            'ID=neon\n'
            'ID_LIKE="ubuntu debian"\n'
            'PRETTY_NAME="KDE neon User Edition 5.8"\n'
            'VERSION_ID="16.04"\n'
            'HOME_URL="http://neon.kde.org/"\n'
            'SUPPORT_URL="http://neon.kde.org/"\n'
            'BUG_REPORT_URL="http://bugs.kde.org/"\n'
            'VERSION_CODENAME=xenial\n'
            'UBUNTU_CODENAME=xenial`\n'
        )

        distro_unknown_no_id_like = (
            'PRETTY_NAME="Make believe 1.0"\n'
            'NAME="Make believe"\n'
            'VERSION_ID="1.0"\n'
            'VERSION="1.0 (rogers)"\n'
            'ID=MakeBelieve`\n'
        )

        ubuntu = sqltoolsservicesetup._get_linux_distro_runtime_id(distro_ubuntu_14_04)
        fedora = sqltoolsservicesetup._get_linux_distro_runtime_id(distro_fedora_23)
        debian = sqltoolsservicesetup._get_linux_distro_runtime_id(distro_debian_8)
        centos = sqltoolsservicesetup._get_linux_distro_runtime_id(distro_centos_7)
        kde_neon = sqltoolsservicesetup._get_linux_distro_runtime_id(distro_kde_neon_5_8)
        unknown = sqltoolsservicesetup._get_linux_distro_runtime_id(distro_unknown_no_id_like)

        self.assertEqual('Ubuntu_14', ubuntu)
        self.assertEqual('Fedora_23', fedora)
        self.assertEqual('Debian_8', debian)
        self.assertEqual('CentOS_7', centos)
        self.assertEqual('Ubuntu_16', kde_neon)
        self.assertEqual(None, unknown)

        #TODO: Add test for checking linux download links

if __name__ == '__main__':
    unittest.main()
