# Installation Guide

## Quick Start
mssql-scritper is installed via pip.  If you know  pip, you can install mssql-scripter using command
```shell
$ pip install mssql-scripter 
```
This command may need to run as sudo if you are installing to the system site packages. mssql-scripter can be 
installed using the --user option, which does not require sudo.
```shell
$ pip install --user mssql-scripter 
```

If you are having installation issues, see the [troubleshooting](#troubleshooting) section for known issues and workarounds.  

### Dependencies

Upon installation, mssql-scripter will detect the operating system or distribution of the host to install the mssqltoolsservice, a platform specific native dependency. Due to this native dependency being detected during the setup.py install, it is recommended that wheel caches not be shared amongst different operating system platforms and distributions. If you upgrade your operating system or distribution, please reinstall mssql-scripter with --no-cache-dir option.
```shell
$ pip install mssql-scripter --no-cache-dir
```

## Detailed Instructions

For operating system specific installs, see one of the following links:

* [macOS](#macos-installation)
* [Linux](#linux-installation)
* [Windows](#windows-installation)

# macOS Installation

Check if pip 9.0 or above is installed using command: 
```shell
$ pip --version
```

If pip is not installed or less than version 9.0, upgrade pip using the following command:

```shell
$ sudo apt-get install python-pip
$ sudo pip install --upgrade pip
```

Install mssql-scripter using command:

```shell
$ sudo pip install mssql-scripter 
```

# Linux Installation

Check if pip 9.0 or above is installed using command: 
```shell
$ pip --version
```

If pip is not installed or less than version 9.0, upgrade pip using the following command:

```shell
$ sudo apt-get install python-pip
$ sudo pip install --upgrade pip
```

Install mssql-scritper using command:

```shell
$ sudo pip install mssql-scripter 
```
If you are using Ubuntu or Debian, you'll need to install the libunwind8 package.  See the [libunwind8 installation steps below](#installing-the-libunwind8-package).

# Windows Installation

Python is not installed by default on Windows.  The latest Python installation package can be downloaded from [here](https://www.python.org/downloads/).  When installing, select the 'Add Python to PATH' option.  Python must be in the PATH environment variable.

Once Python is installed and in the PATH environment variable, open a command prompt, and install mssql-scripter using the command:
```shell
C:\> pip install mssql-scripter 
```

# Troubleshooting

If you're having installation issues, please check the below known issues and workarounds.  If you're having a different issue, please check the [issues](https://github.com/Microsoft/sql-xplat-cli/issues) page to see if the issue has already been reported.  If you don't see your issue there, filing a new issue would be appreciated.

## Could not find version that satifies the requirement mssql-scripter
If you see the above error running `pip install mssql-scripter`, this means the pip version used is out-of-date.  Upgrade pip using the command:
```shell
$ sudo apt-get install python-pip
$ sudo pip install --upgrade pip
```

## Ubuntu 14 & 17, Debian 8 - libunwind.so.8: cannot open shared object file
If you encounter the below error running mssql-scripter, this means the libunwind8 package is not installed.
```shell
Failed to load /usr/local/lib/python2.7/dist-packages/mssqltoolsservice/bin/libcoreclr.so, error 
libunwind.so.8: cannot open shared object file: No such file or directory
```

## Installing the libunwind8 package

### Ubuntu 14 & 17
Run commands
```shell
$ sudo apt-get update
$ sudo apt-get install libunwind8
```

### Debian 8
The file `/etc/apt/sources.list' needs to updated with the following line
```
deb http://ftp.us.debian.org/debian/ jessie main
```
Then run commands:
```shell
$ sudo apt-get update
$ sudo apt-get install libunwind8
```
