# mssql-scripter 0.1

We're excited to introduce mssql-scripter, a multi-platform command line experience for scripting SQL Server databases.

## Installation

Currently, we only support installation by building and installing from a local pip installation package.  First, 
[Configuring Your Machine](https://github.com/Microsoft/sql-xplat-cli/blob/dev/doc/testing_local_install.md), and then 
run through the [Testing local install](https://github.com/Microsoft/sql-xplat-cli/blob/dev/doc/testing_local_install.md) instructions.

## Usage

For usage and help content, pass in the `-h` parameter, for example:

```bash
$ mssql-scripter -h
```
Here are a example commands that run against the AdventureWorks database:

```bash
# script the database schema to stdout
$ mssql-scripter -S localhost -d AdventureWorks -U sa 

# script the database schema and data to a file
$ mssql-scripter -S localhost -d AdventureWorks -U sa --schema-and-data  > ./adventureworks.sql

# script the database schema and data to a stdout
$ mssql-scripter -S localhost -d AdventureWorks -U sa --include-objects Employee

# script the dbo schema to a file
$ mssql-scripter -S localhost -d AdventureWorks -U sa --include-objects dbo. > ./dboschema.sql 

```
## Reporting issues and feedback

If you encounter any bugs with the tool please file an issue in the [Issues](https://github.com/Microsoft/sql-xplat-cli/issues) section of our GitHub repo.

## Developer Setup
If you would like to setup a development environment and contribute to mssql-scritper, see 
[Configuring Your Machine](https://github.com/Microsoft/sql-xplat-cli/blob/dev/doc/configuring_your_machine.md).

To test out changes, see [Testing local install](https://github.com/Microsoft/sql-xplat-cli/blob/dev/doc/testing_local_install.md). 

## Code of Conduct

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).

For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

## License

mssql-scritper is licensed under the [MIT license](https://github.com/Microsoft/sql-xplat-cli/blob/dev/LICENSE.txt).
