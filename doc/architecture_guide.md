# mssql-scripter Architecture

The three core components of mssql-scripter are:
* Python Client
* Scripting Service
* SqlScriptPublishModel

## Python Client
The Python client is script that orchestrates the scripting operation. It's responsible for: 
- Parsing the command line options
- Starting the SqlToolsService process
- Issuing the scripting request to the Scripting Service
- Responding to the Scripting Service events which report progress and completion
- Piping the script results to STDIO
	
## Scripting Service 
The  Scripter Service is hosted by the SqlToolsService, which is itself a [self-contained](https://docs.microsoft.com/en-us/dotnet/articles/core/deploying/#self-contained-deployments-scd) [.NET Core](https://docs.microsoft.com/en-us/dotnet/articles/core) console application.  The Scripting Service is responsible for:
- Exposing the JSON-RPC endpoint to handle scripting requests
- Instantiating the SqlScriptPublishModel to execute a scripting request
- Forwarding events from the SqlScriptPublishModel to clients over JSON-RPC   

#### NOTE
The SqlToolsService is used by other cross platform SQL tools, such as the [Microsoft/vscode-mssql](https://github.com/Microsoft/vscode-mssql) extension.  The SqlToolsService is an open source project and hosted on github at [Microsoft/sqltoolsservice](https://github.com/Microsoft/sqltoolsservice).

## SqlScriptPublishModel 
The SqlScriptPublishModel is the component used by the Scripting Service to drive the scripting operation.  It uses the SQL Server Management Objects (SMO) framework, to generate the underlying scripts for database.  It's responsible for:  
- Running the scripting operations using SMO
- Send progress events as the scripting operation makes progress

### SQL Server Management Objects (SMO) 
The [SQL Server Management Objects](https://docs.microsoft.com/en-us/sql/relational-databases/server-management-objects-smo/overview-smo) library is designed for programmatic management of SQL Server.  One of the many features it provides is scripting interface.  SMO can be used to discover dependencies, understand the relationships between objects, and generate a .sql script that can re-create the objects in a database. 

#### NOTE
The SqlScriptPublishModel and SMO are the same components used by the [Scripting Wizard](https://docs.microsoft.com/en-us/sql/relational-databases/scripting/generate-scripts-sql-server-management-studio) in [SQL Server Management Studio (SSMS)](https://docs.microsoft.com/en-us/sql/ssms/sql-server-management-studio-ssms).

# Sequence Diagram

![PlantUML model](http://www.plantuml.com/plantuml/png/tLDBJiCm4Dtx5AFkqmDK4H8g4XAYj10ku2P3Qycn4tjI54wFxNnAurIKBJjxtipaVHmI915AQskPsDo8Yj10XdM3AaTu4FnWUCaOpqaRM5psBO1Rw2uirugCbb1oePPLwn5_7EjPBT-rbdOj1IgAoXcQayYHEKnG2rbOAjHXMgzb1-sQlHJskD45oX7SR5d1YU-vHLXahy_WfptD-mm6O6XUB9qI-10IWmf_OApJ0ibTu0uhC8s2ggMZLYnK778fnFKe_9mMsUJ-OwmNvEOiSKDG6PsZjTVNzvn6ONEx9sxDJ3rbsvVaRRS6uwErDDsI9h7dWP87BgEBljQnZdDnD1vHeU647HYup_Jv1Pjjp9hvQkhGKSOAkEAo_K9m1TarEDodTnuFqDcdWMQQ95TvkXGEniSGsPBC93Tqdrt5Kt3c5xhmt_ZESFFlnMSPFvFqkfo_YSzrMKaal4tyq1s9l-aNrLNqX_PcICsBxZmYlJ_ES55XXv5sImhT4Fi6)
