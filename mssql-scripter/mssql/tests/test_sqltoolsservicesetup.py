# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import unittest
import sqltoolsservicesetup


class TestSqlToolsServiceSetup(unittest.TestCase):
    """
        Sql tools service setup tests.
    """

    def test_native_dependency_download_path(self):
        """
            Verifies correct download link is return based on platform and architecture.
        """
        windows_32_id = sqltoolsservicesetup._get_runtime_id(
            system=u'Windows', architecture=u'32bit')
        windows_64_id = sqltoolsservicesetup._get_runtime_id(
            system=u'Windows', architecture=u'64bit')
        mac_64_id = sqltoolsservicesetup._get_runtime_id(
            system=u'Darwin', architecture=u'64bit')

        self.assertEqual(windows_32_id, u'Windows_7_86')
        self.assertEqual(windows_64_id, u'Windows_7_64')
        self.assertEqual(mac_64_id, u'OSX_10_11_64')

        windows_32_link = sqltoolsservicesetup.get_download_url(windows_32_id)
        windows_64_link = sqltoolsservicesetup.get_download_url(windows_64_id)
        mac_64_link = sqltoolsservicesetup.get_download_url(mac_64_id)

        self.assertTrue(
            u'microsoft.sqltools.servicelayer-win-x86-netcoreapp1.0.zip' in windows_32_link)
        self.assertTrue(
            u'microsoft.sqltools.servicelayer-win-x64-netcoreapp1.0.zip' in windows_64_link)
        self.assertTrue(
            u'microsoft.sqltools.servicelayer-osx-x64-netcoreapp1.0.tar.gz' in mac_64_link)

    def test_get_linux_distro_runtime_id(self):
        """
            Verifies Linux distro runtime id can be extracted from contents found in /etc/os-release.
        """
        # Copied from /etc/os-release on Ubuntu 14.04.
        distro_ubuntu_14_04 = (
            u'NAME="Ubuntu"\n'
            u'VERSION="14.04.5 LTS, Trusty Tahr"\n'
            u'ID=ubuntu\n'
            u'ID_LIKE=debian\n'
            u'PRETTY_NAME="Ubuntu 14.04.5 LTS"\n'
            u'VERSION_ID="14.04"\n'
            u'HOME_URL="http://www.ubuntu.com/"\n'
            u'SUPPORT_URL="http://help.ubuntu.com/"\n'
            u'BUG_REPORT_URL="http://bugs.launchpad.net/ubuntu/"\n'
        )
        # Copied from /etc/os-release on Fedora 23.
        distro_fedora_23 = (
            u'NAME=Fedora\n'
            u'VERSION="23 (Workstation Edition)"\n'
            u'ID=fedora\n'
            u'VERSION_ID=23\n'
            u'PRETTY_NAME="Fedora 23 (Workstation Edition)"\n'
            u'ANSI_COLOR="0;34"\n'
            u'CPE_NAME="cpe:/o:fedoraproject:fedora:23"\n'
            u'HOME_URL="https://fedoraproject.org/"\n'
            u'BUG_REPORT_URL="https://bugzilla.redhat.com/"\n'
            u'REDHAT_BUGZILLA_PRODUCT="Fedora"\n'
            u'REDHAT_BUGZILLA_PRODUCT_VERSION=23\n'
            u'REDHAT_SUPPORT_PRODUCT="Fedora"\n'
            u'REDHAT_SUPPORT_PRODUCT_VERSION=23\n'
            u'PRIVACY_POLICY_URL=https://fedoraproject.org/wiki/Legal:PrivacyPolicy\n'
            u'VARIANT="Workstation Edition"\n'
            u'VARIANT_ID=workstation`\n')

        # Copied from /etc/os-release on Debian 8.
        distro_debian_8 = (
            u'PRETTY_NAME="Debian GNU/Linux 8 (jessie)"\n'
            u'NAME="Debian GNU/Linux"\n'
            u'VERSION_ID="8"\n'
            u'VERSION="8 (jessie)"\n'
            u'ID=debian\n'
            u'HOME_URL="http://www.debian.org/"\n'
            u'SUPPORT_URL="http://www.debian.org/support"\n'
            u'BUG_REPORT_URL="https://bugs.debian.org/"`;\n'
        )
        # Copied from /etc/os-release on CentOS 7.
        distro_centos_7 = (
            u'NAME="CentOS Linux"\n'
            u'VERSION="7 (Core)"\n'
            u'ID="centos"\n'
            u'ID_LIKE="rhel fedora"\n'
            u'VERSION_ID="7"\n'
            u'PRETTY_NAME="CentOS Linux 7 (Core)"\n'
            u'ANSI_COLOR="0;31"\n'
            u'CPE_NAME="cpe:/o:centos:centos:7"\n'
            u'HOME_URL="https://www.centos.org/"\n'
            u'BUG_REPORT_URL="https://bugs.centos.org/"\n'
            u'CENTOS_MANTISBT_PROJECT="CentOS-7"\n'
            u'CENTOS_MANTISBT_PROJECT_VERSION="7"\n'
            u'REDHAT_SUPPORT_PRODUCT="centos"\n'
            u'REDHAT_SUPPORT_PRODUCT_VERSION="7"`\n'
        )
        # Copied from /etc/os-release on KDE Neon 5.8.
        distro_kde_neon_5_8 = (
            u'NAME="KDE neon"\n'
            u'VERSION="5.8"\n'
            u'ID=neon\n'
            u'ID_LIKE="ubuntu debian"\n'
            u'PRETTY_NAME="KDE neon User Edition 5.8"\n'
            u'VERSION_ID="16.04"\n'
            u'HOME_URL="http://neon.kde.org/"\n'
            u'SUPPORT_URL="http://neon.kde.org/"\n'
            u'BUG_REPORT_URL="http://bugs.kde.org/"\n'
            u'VERSION_CODENAME=xenial\n'
            u'UBUNTU_CODENAME=xenial`\n'
        )

        distro_unknown_no_id_like = (
            u'PRETTY_NAME="Make believe 1.0"\n'
            u'NAME="Make believe"\n'
            u'VERSION_ID="1.0"\n'
            u'VERSION="1.0 (rogers)"\n'
            u'ID=MakeBelieve`\n'
        )

        ubuntu = sqltoolsservicesetup._get_linux_distro_runtime_id(
            distro_ubuntu_14_04)
        fedora = sqltoolsservicesetup._get_linux_distro_runtime_id(
            distro_fedora_23)
        debian = sqltoolsservicesetup._get_linux_distro_runtime_id(
            distro_debian_8)
        centos = sqltoolsservicesetup._get_linux_distro_runtime_id(
            distro_centos_7)
        kde_neon = sqltoolsservicesetup._get_linux_distro_runtime_id(
            distro_kde_neon_5_8)
        unknown = sqltoolsservicesetup._get_linux_distro_runtime_id(
            distro_unknown_no_id_like)

        self.assertEqual(u'Ubuntu_14', ubuntu)
        self.assertEqual(u'Fedora_23', fedora)
        self.assertEqual(u'Debian_8', debian)
        self.assertEqual(u'CentOS_7', centos)
        self.assertEqual(u'Ubuntu_16', kde_neon)
        self.assertEqual(None, unknown)



if __name__ == u'__main__':
    unittest.main()
