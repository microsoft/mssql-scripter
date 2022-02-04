# Usage Guide
Contents:

[Options](#options)

[Examples](#examples)

[Environment Variables](#environment-variables)

## Description
mssql-scripter is the multiplatform command line equivalent of the widely used Generate Scripts Wizard experience in SSMS.
 
You can use mssql-scripter on Linux, macOS, and Windows to generate data definition language (DDL) and data manipulation language (DML) T-SQL scripts for database objects in SQL Server running anywhere, Azure SQL Database, and Azure SQL Data Warehouse. You can save the generated T-SQL script to a .sql file or pipe it to standard *nix utilities (for example, sed, awk, grep) for further transformations. You can edit the generated script or check it into source control and subsequently execute the script in your existing SQL database deployment processes and DevOps pipelines with standard multiplatform SQL command line tools such as sqlcmd.

## Options
For option parameters, pass in '-h': 

    $ mssql-scripter -h
    usage: mssql-scripter [-h] [--connection-string  | -S ] [-d] [-U] [-P] [-f]
                      [--file-per-object] [--data-only | --schema-and-data]
                      [--script-create | --script-drop | --script-drop-create]
                      [--target-server-version {2005,2008,2008R2,2012,2014,2016,vNext,AzureDB,AzureDW}]
                      [--target-server-edition {Standard,Personal,Express,Enterprise,Stretch}]
                      [--include-objects [[...]]] [--exclude-objects [[...]]]
                      [--include-schemas [[...]]] [--exclude-schemas [[...]]]
                      [--include-types [[...]]] [--exclude-types [[...]]]
                      [--ansi-padding] [--append] [--check-for-existence] [-r]
                      [--convert-uddts] [--include-dependencies]
                      [--exclude-headers] [--constraint-names]
                      [--unsupported-statements]
                      [--disable-schema-qualification] [--bindings]
                      [--collation] [--exclude-defaults]
                      [--exclude-extended-properties] [--logins]
                      [--object-permissions] [--owner]
                      [--exclude-use-database] [--statistics]
                      [--change-tracking] [--exclude-check-constraints]
                      [--data-compressions] [--exclude-foreign-keys]
                      [--exclude-full-text-indexes] [--exclude-indexes]
                      [--exclude-primary-keys] [--exclude-triggers]
                      [--exclude-unique-keys] [--display-progress]
                      [--enable-toolsservice-logging] [--version]

    Microsoft SQL Server Scripter Command Line Tool. Version 1.0.0a14

    optional arguments:
      -h, --help            show this help message and exit
      --connection-string   Connection string of database to script. If connection
                            string and server are not supplied, defaults to value
                            in environment variable
                            MSSQL_SCRIPTER_CONNECTION_STRING.
      -S , --server         Server name.
      -d , --database       Database name.
      -U , --user           Login ID for server.
      -P , --password       If not supplied, defaults to value in environment
                            variable MSSQL_SCRIPTER_PASSWORD.
      -f , --file-path      File to script out to or directory name if scripting
                            file per object.
      --file-per-object     By default script to a single file. If supplied and
                            given a directory for --file-path, script a file per
                            object to that directory.
      --data-only           By default only the schema is scripted. if supplied,
                            generate scripts that contains data only.
      --schema-and-data     By default only the schema is scripted. if supplied,
                            generate scripts that contain schema and data.
      --script-create       Script object CREATE statements.
      --script-drop         Script object DROP statements.
      --script-drop-create  Script object CREATE and DROP statements.
      --target-server-version {2005,2008,2008R2,2012,2014,2016,vNext,AzureDB,AzureDW}
                            Script only features compatible with the specified SQL
                            Version.
      --target-server-edition {Standard,Personal,Express,Enterprise,Stretch}
                            Script only features compatible with the specified SQL
                            Server database edition.
      --include-objects [ [ ...]]
                            Database objects to include in script.
      --exclude-objects [ [ ...]]
                            Database objects to exclude from script.
      --include-schemas [ [ ...]]
                            Database objects of this schema to include in script.
      --exclude-schemas [ [ ...]]
                            Database objects of this schema to exclude from
                            script.
      --include-types [ [ ...]]
                            Database objects of this type to include in script.
      --exclude-types [ [ ...]]
                            Database objects of this type to exclude from script.
      --ansi-padding        Generates ANSI Padding statements.
      --append              Append script to file.
      --check-for-existence
                            Check that an object with the given name exists before
                            dropping or altering or that an object with the given
                            name does not exist before creating.
      -r, --continue-on-error
                            Continue scripting on error.
      --convert-uddts       Convert user-defined data types to base types.
      --include-dependencies
                            Generate script for the dependent objects for each
                            object scripted.
      --exclude-headers     Exclude descriptive headers for each object scripted.
      --constraint-names    Include system constraint names to enforce declarative
                            referential integrity.
      --unsupported-statements
                            Include statements in the script that are not
                            supported on the target SQL Server Version.
      --disable-schema-qualification
                            Do not prefix object names with the object schema.
      --bindings            Script options to set binding options.
      --collation           Script the objects that use collation.
      --exclude-defaults    Do not script the default values.
      --exclude-extended-properties
                            Exclude extended properties for each object scripted.
      --logins              Script all logins available on the server, passwords
                            will not be scripted.
      --object-permissions  Generate object-level permissions.
      --owner               Script owner for the objects.
      --exclude-use-database
                            Do not generate USE DATABASE statement.
      --statistics          Script all statistics.
      --change-tracking     Script the change tracking information.
      --exclude-check-constraints
                            Exclude check constraints for each table or view
                            scripted.
      --data-compressions   Script the data compression information.
      --exclude-foreign-keys
                            Exclude foreign keys for each table scripted.
      --exclude-full-text-indexes
                            Exclude full-text indexes for each table or indexed
                            view scripted.
      --exclude-indexes     Exclude indexes (XML and clustered) for each table or
                            indexed view scripted.
      --exclude-primary-keys
                            Exclude primary keys for each table or view scripted.
      --exclude-triggers    Exclude triggers for each table or view scripted.
      --exclude-unique-keys
                            Exclude unique keys for each table or view scripted.
      --display-progress    Display scripting progress.
      --enable-toolsservice-logging
                            Enable verbose logging.
      --version             show program's version number and exit
      
## Examples
Below are example commands that run against the AdventureWorks database. Here is the list of examples:

[Dump database object schema](#dump-database-object-schema)

[Dump database object data](#dump-database-object-data)

[Dump database object schema and data](#dump-the-database-object-schema-and-data)

[Include database objects](#include-database-objects)

[Exclude database objects](#exclude-database-objects)

[Include database object types](#include-database-object-types)

[Target server version](#target-server-version)

[Target server edition](#target-server-edition)

[Pipe a generated script to sed](#pipe-a-generated-script-to-sed)

[Script data to a file](#script-data-to-a-file)




### Dump database object schema

    # generate DDL scripts for all objects in the Adventureworks database and save the script to a file
    mssql-scripter -S localhost -d AdventureWorks -U sa
    
    # alternatively, specify the schema only flag to generate DDL scripts for all objects in the Adventureworks database and save the script to a file
    mssql-scripter -S localhost -d AdventureWorks -U sa -f ./adventureworks.sql

### Dump database object data

    # generate DDL scripts for all objects in the Adventureworks database and save the script to stdout.
    mssql-scripter -S localhost -d AdventureWorks -U sa --data-only

### Dump the database object schema and data

    # script the database schema and data piped to a file.
    mssql-scripter -S localhost -d AdventureWorks -U sa --schema-and-data  > ./adventureworks.sql

    # execute the generated above script with sqlcmd
    sqlcmd -S mytestserver -U sa -i ./adventureworks.sql
    
### Include database objects

    # generate DDL scripts for objects that contain 'Employee' in their name to stdout
    mssql-scripter -S localhost -d AdventureWorks -U sa --include-objects Employee

    # generate DDL scripts for the dbo schema and pipe the output to a file
    mssql-scripter -S localhost -d AdventureWorks -U sa --include-objects dbo. > ./dboschema.sql

### Exclude database objects
   
    # generate DDL scripts for objects that do not contain 'Sale' in their name to stdout
    mssql-scripter -S localhost -d AdventureWorks -U sa --exclude-objects Sale

### Include database object types
   
    # generate DDL scripts for stored procedures to stdout  
    # The list of object types is specified in the DatabaseObjectTypes Enum of Microsoft.SqlServer.Management.Smo 
    # https://docs.microsoft.com/en-us/dotnet/api/microsoft.sqlserver.management.smo.databaseobjecttypes?view=sql-smo-160
    mssql-scripter -S localhost -d AdventureWorks -U sa --include-types StoredProcedure

### Target server version
    
    # specify the version of SQL Server the script will be run against
    mssql-scripter -S myServer -d AdventureWorks -U myUser –-target-server-version "AzureDB" > myData.sql

### Target server edition

    # specify the edition of SQL Server the script will be run against
    mssql-scripter -S localhost -d AdventureWorks -U myUser –-target-server-edition "Enterprise" > myData.sql

### Pipe a generated script to sed
Note this example is for Linux and macOS usage.

    # change a schema name in the generated DDL script
    # 1) generate DDL scripts for all objects in the Adventureworks database
    # 2) pipe generated script to sed and change all occurrences of SalesLT to SalesLT_test and save the script to a file
    $ mssql-scripter -S localhost -d Adventureworks -U sa | sed -e "s/SalesLT./SalesLT_test./g" > adventureworks_SalesLT_test.sql 

### Script data to a file
   
    # script all the data to a file.
    mssql-scripter -S localhost -d AdventureWorks -U sa --data-only > ./adventureworks-data.sql 
    

## Environment Variables
You can set environment variables for your connection string through the following steps:


    # (linux/bash)
    # set environment variable MSSQL_SCRIPTER_CONNECTION_STRING with a connection string.
    $ export MSSQL_SCRIPTER_CONNECTION_STRING='Server=myserver;Database=mydb;User Id=myuser;Password=mypassword;'
    $ mssql-scripter

    # (linux/bash)
    # set environment variable MSSQL_SCRIPTER_PASSWORD so no password input is required.
    $ export MSSQL_SCRIPTER_PASSWORD='[PLACEHOLDER]'
    $ mssql-scripter -S localhost -d AdventureWorks -U sa

    # (windows)
    # set environment variable MSSQL_SCRIPTER_CONNECTION_STRING with a connection string.
    setx MSSQL_SCRIPTER_CONNECTION_STRING 'Server=myserver;Database=mydb;User Id=myuser;Password=mypassword;'
    # note: you must start a new PS session for the change to take effect
    mssql-scripter
    
    # (windows)
    # set environment variable MSSQL_SCRIPTER_PASSWORD so no password input is required.
    setx MSSQL_SCRIPTER_PASSWORD mypassword
    # note: you must start a new PS session for the change to take effect
    $ mssql-scripter -S localhost -d AdventureWorks -U sa
   
