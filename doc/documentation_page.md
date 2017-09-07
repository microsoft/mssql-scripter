# Get Started with mssql-scripter

mssql-scripter is the multiplatform command line equivalent of the widely used Generate Scripts Wizard experience in SSMS.

You can use mssql-scripter on Linux, macOS, and Windows to generate data definition language (DDL) and data manipulation language (DML) T-SQL scripts for database objects in SQL Server running anywhere, Azure SQL Database, and Azure SQL Data Warehouse. You can save the generated T-SQL script to a .sql file or pipe it to standard *nix utilities (for example, sed, awk, grep) for further transformations. You can edit the generated script or check it into source control and subsequently execute the script in your existing SQL database deployment processes and DevOps pipelines with standard multiplatform SQL command line tools such as sqlcmd.

## Install

For information about installation, please see the LINK/install guide/LINK.

The examples in this guide use the Adventureworks sample database. You can download the sample [here](https://www.microsoft.com/en-us/download/details.aspx?id=49502).

## Generate scripts
Use mssql-scripter to generate scripts for database schema and/or data by including specific objects, targeting server versions/editions,  and piping the script to files.

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
    mssql-scripter -S localhost -d Adventureworks -U sa | sed -e "s/SalesLT./SalesLT_test./g" > adventureworks_SalesLT_test.sql 

### Script data to a file
   
    # script all the data to a file.
    mssql-scripter -S localhost -d AdventureWorks -U sa --data-only > ./adventureworks-data.sql 

### Set environment variables
You can set environment variables for your connection string through the following steps:


    # set environment variable MSSQL_SCRIPTER_CONNECTION_STRING with a connection string.
    export MSSQL_SCRIPTER_CONNECTION_STRING='Server=myserver;Database=mydb;User Id=myuser;Password=mypassword;'
    mssql-scripter

    # set environment variable MSSQL_SCRIPTER_PASSWORD so no password input is required.
    export MSSQL_SCRIPTER_PASSWORD='ABC123'
    mssql-scripter -S localhost -d AdventureWorks -U sa
    
 ## Run your scripts using sqlcmd
 Now that you have generated a script for your database objects, you can execute the script using sqlcmd such as in the example below.
 
    # script all the data to a file.
    mssql-scripter -S localhost -d AdventureWorks -U sa --data-only > ./adventureworks-data.sql
    sqlcmd -S localhost -d AdventureWorks -U sa -i`./adventureworks-data.sql
 
 You can find more details on using sqlcmd [here](https://docs.microsoft.com/en-us/sql/relational-databases/scripting/sqlcmd-use-the-utility).
