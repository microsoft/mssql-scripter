.. image:: https://travis-ci.org/Microsoft/sql-xplat-cli.svg?branch=dev
    :target: https://travis-ci.org/Microsoft/sql-xplat-cli

.. image:: https://ci.appveyor.com/api/projects/status/vpm8p71265ijytqs/branch/dev?svg=true
    :target: https://ci.appveyor.com/project/MrMeemus/sql-xplat-cli

.. image:: https://codecov.io/gh/Microsoft/sql-xplat-cli/branch/dev/graph/badge.svg?token=M96uWrHOIu
    :target: https://codecov.io/gh/Microsoft/sql-xplat-cli/branch/dev

.. image:: https://badge.fury.io/py/mssql-scripter.svg
    :target: https://pypi.python.org/pypi/mssql-scripter

.. image:: https://img.shields.io/pypi/pyversions/mssql-scripter.svg
    :target: https://travis-ci.org/Microsoft/sql-xplat-cli

mssql-scripter
===============
We’re excited to introduce mssql-scripter, a multi-platform command line
experience for scripting SQL Server databases.

mssql-scripter is the multiplatform command line equivalent of the widely used Generate Scripts Wizard experience in SSMS. You can use mssql-scripter on Linux, macOS, and Windows to generate data definition language (DDL) and data manipulation language (DML) T-SQL scripts for database objects in SQL Server running anywhere, Azure SQL Database, and Azure SQL Data Warehouse. You can save the generated T-SQL script to a .sql file or pipe it to standard nix utilities (for example, sed, awk, grep) for further transformations. You can edit the generated script or check it into source control and subsequently execute the script in your existing SQL database deployment processes and DevOps pipelines with standard multiplatform SQL command line tools such as sqlcmd.
 
mssql-scripter is built using Python and incorporates the usability principles of the new Azure CLI 2.0 tools. 

Installation
------------

.. code:: bash

    $ pip install mssql-scripter

Please refer to the `installation guide`_ for detailed install instructions. 

Usage
-----

Please refer to the `usage guide`_ for details on options and example usage.

For general help content, pass in the ``-h`` parameter:

.. code:: bash

    $ mssql-scripter -h

Contributing
-----------------------------
If you would like to contribute to the project, please refer to the `development guide`_.

Reporting issues and feedback
-----------------------------

If you encounter any bugs with the tool please file an issue in the
`Issues`_ section of our GitHub repo.

Code of Conduct
---------------

This project has adopted the `Microsoft Open Source Code of Conduct`_.

For more information see the `Code of Conduct FAQ`_ or contact
opencode@microsoft.com with any additional questions or comments.

License
-------

mssql-scritper is licensed under the `MIT license`_.

.. _installation guide: doc/installation_guide.md
.. _development guide: doc/development_guide.md
.. _usage guide: doc/usage_guide.md
.. _Issues: https://github.com/Microsoft/sql-xplat-cli/issues
.. _Microsoft Open Source Code of Conduct: https://opensource.microsoft.com/codeofconduct/
.. _Code of Conduct FAQ: https://opensource.microsoft.com/codeofconduct/faq/
.. _MIT license: https://github.com/Microsoft/sql-xplat-cli/blob/dev/LI
