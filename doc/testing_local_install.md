Testing local install
=====================
 This guide will provide details on building and 
installing of Mssql-Scripter in both a virtual environment and a machine environment. 

#### Building local package
1. Execute the following in \<clone root>:

        python setup.py sdist
    
2. Delete the generated egg file in \<clone root>:

###### Windows
    rmdir /s mssql_scripter.egg-info
###### OSX/Ubuntu (bash)
    rm -rf mssql_scripter.egg-info

#### Installing mssql-scripter package
1. Execute the following in \<clone root>/dist:

###### Virtual Environment

    pip install mssql-scripter-0.1.1.dev0.tar.gz
    
###### User Account

    pip install --user mssql-scripter-0.1.1.dev0.tar.gz

#### Running mssql-scripter


    mssql-scripter -h

if the command above fails, ensure your python scripts folder is added to your system path. 

#### Uninstall 

    pip uninstall mssql-scripter
###### Windows

    rmdir /s <Python-Version>\Lib\site-packages\mssqlscripter\sqltoolsservice

###### OSX/Ubuntu (bash)


    rm -rf <Python-Version>/Lib/site-packages/mssqlscripter/sqltoolsservice