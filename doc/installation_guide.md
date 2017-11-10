# Installation Guide

## Quick Start
mssql-scripter is installed via pip.  If you know pip, you can install mssql-scripter using command
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

Check if Python is installed using command:
```shell
$ python --version
```
If Python is not installed or less than version 2.7, upgrade Python using the following command:
```shell
$ sudo brew install python
```

Check if pip 9.0 or above is installed using command: 
```shell
$ pip --version
```

If pip is not installed or less than version 9.0, upgrade pip using the following command:

```shell
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

Install mssql-scripter using command:

```shell
$ sudo pip install mssql-scripter 
```
If you are using Ubuntu or Debian, you'll need to install the libunwind8 package.  See the [libunwind8 installation steps below](#installing-the-libunwind8-package).

If you are using RHEL, you'll need to install the icu package.  See the [icu installation steps below](#installing-the-icu-package).

# Windows Installation

Python is not installed by default on Windows.  The latest Python installation package can be downloaded from [here](https://www.python.org/downloads/).  When installing, select the 'Add Python to PATH' option.  Python must be in the PATH environment variable.

Once Python is installed and in the PATH environment variable, open a command prompt, and install mssql-scripter using the command:
```shell
C:\> pip install mssql-scripter 
```

# Troubleshooting

If you're having installation issues, please check the below known issues and workarounds.  If you're having a different issue, please check the [issues](https://github.com/Microsoft/mssql-scripter/issues) page to see if the issue has already been reported.  If you don't see your issue there, filing a new issue would be appreciated.

## Error: No module named mssqlscripter
If the installation was successful and this error message is encountered, this may be caused by different versions of python in the environment.
i.e Used python 3.6 to install mssql-scripter, but PATH has python 2.7 so it uses the python 2.7 interpreter which has no visibility to packages installed into python 3.6.

The workaround to prevent this is to use a virtual environment, which will provide a isolated environment that is tied to a specific python version.
More information can be found at:

- [Virtual Environment Info](virtual_environment_info.md)

- [Development guide](development_guide.md#Environment_Setup)

## Error: Could not find version that satisfies the requirement mssql-scripter
If you see the above error running `pip install mssql-scripter`, this means the pip version used is out-of-date.  Upgrade pip using the command:
```shell
$ sudo apt-get install python-pip
$ sudo pip install --upgrade pip
```

## Error: System.DllNotFoundException: Unable to load DLL 'System.Security.Cryptography.Native': The specified module could not be found.
If you encounter this error on MacOS, this means you need the latest version of OpenSSL. To update:
```shell
$ brew update
$ brew install openssl
$ mkdir -p /usr/local/lib
$ ln -s /usr/local/opt/openssl/lib/libcrypto.1.0.0.dylib /usr/local/lib/
$ ln -s /usr/local/opt/openssl/lib/libssl.1.0.0.dylib /usr/local/lib/
```

## Error: libunwind.so.8: cannot open shared object file
If you encounter the below error running mssql-scripter, this means the libunwind8 package is not installed.  This error has been seen
on Ubuntu 14 & 17, Debian 8.
```shell
Failed to load /usr/local/lib/python2.7/dist-packages/mssqltoolsservice/bin/libcoreclr.so, error 
libunwind.so.8: cannot open shared object file: No such file or directory
```

## Error: Failed to initialize CoreCLR, HRESULT: 0x80131500 on RHEL
If you encounter this error running mssql-scripter Red Hat Enterprise Linux, it could be due to the icu package not being installed.  See the [icu installation steps below](#installing-the-icu-package).

## Installing the libunwind8 package

### Ubuntu 14 & 17
Run commands
```shell
$ sudo apt-get update
$ sudo apt-get install libunwind8
```

### Debian 8
The file `/etc/apt/sources.list' needs to be updated with the following line
```
deb http://ftp.us.debian.org/debian/ jessie main
```
Then run commands:
```shell
$ sudo apt-get update
$ sudo apt-get install libunwind8
```

## Installing the icu package

### RHEL 7.3
Run commands
```shell
$ sudo sudo yum install icu
```
