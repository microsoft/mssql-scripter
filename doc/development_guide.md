Development Guide
=================

## Table of Contents
1. [Preparing your machine](#Preparing_machine)
1. [Environment Setup](#Environment_Setup)
2. [Configuring IDE](#Configure_IDE)
3. [Running Tests](#Running_Tests)
4. [Running mssql-scripter](#Run_mssql-scripter)
4. [Packaging](pypi_release_steps.md)


mssql-scripter sources are located on GitHub (https://github.com/Microsoft/sql-xplat-cli). In order to contribute to the project, you are expected to: 
-	Have a GitHub account. For Microsoft contributors, follow the guidelines on https://opensourcehub.microsoft.com/ to create, configure and link your account
-	Fork the  https://github.com/Microsoft/sql-xplat-clirepository into your private GitHub account
-	Create pull requests against the https://github.com/Microsoft/sql-xplat-cli repository to get your code changes merged into the project repository.

## <a name="Preparing_Machine"></a>1. Preparing your machine
1.	Install latest Python from http://python.org. Please note that the version of Python that comes preinstalled on OSX is 2.7. 
    #### Windows
    - The latest Python installation package can be downloaded from [here](https://www.python.org/downloads/).  
    - During installation, select the 'Add Python to PATH' option.  Python must be in the PATH environment variable.
    
2. Clone the repo from [https://github.com/Microsoft/sql-xplat-cli](https://github.com/Microsoft/sql-xplat-cli)

## <a name="Environment_Setup"></a>2. Environment Setup
When developing on a Python project, it is recommended to do so in a virtual environment. A virtual environment is a sandbox that maintains a copy of all libraries necessary to run python in a isolated environment without interfering with the system or global python. For more information on virtual environments, go to [Virtual Environment Info](docs/virtual_environment_info.md).

If not developing in a virtual environment, please proceed to [Development Setup](#Development) 
### Virtual Environment
1. Create a virtual environment in a subdirectory of your `<clone_root>`, using `<clone_root>/env` as a example:
 
     ##### Windows
    ```BatchFile
    python -m venv <clone_root>\env
    ```
    ##### MacOS/Linux (bash)
    ```Shell
    python –m venv <clone_root>/env
    ```
2.  Activate the env virtual environment by running:

    ##### Windows
    ```BatchFile
    <clone_root>\env\scripts\activate.bat
    ```
    ##### MacOS/Linux (bash)
    ```Shell
    . <clone_root>/env/bin/activate
    ```
3. To deactivate the virtual environment:

    ##### Windows
    ```BatchFile
    <clone_root>\env\scripts\deactivate.bat
    ```
    ##### MacOS/Linux (bash)
    ```Shell
    deactivate
    ```
### <a name="Development"></a>Development Setup
General development steps that apply to both a virtual environment or a global environment. If working in a virtual environment, do ensure the virtual environment is activated.
1.  Add `<clone_root>` to your PYTHONPATH environment variable:

    ##### Windows
    ```BatchFile
    set PYTHONPATH=<clone_root>;%PYTHONPATH%
    ```
    ##### MacOS/Linux (bash)
    ```Shell
    export PYTHONPATH=<clone_root>:${PYTHONPATH}
    ```
2.	Install the dependencies:
    ```Shell
    python <clone_root>/dev_setup.py clean
    ```
## <a name="Configure_IDE"></a>3. Configuring your IDE
#### Visual Studio (Windows only)
1.	Install [Python Tools for Visual Studio](https://github.com/Microsoft/PTVS)
2.	Open the <clone_root>\sql-xplat-cli.pyproj project in Visual Studio


#### Visual Studio Code (Any platform)

1.	Install VS Code
2.	Install the the VS Code [Python extension](https://marketplace.visualstudio.com/items?itemName=donjayamanne.python)

The repo has a launch.json file that will launch the version of Python that is first on your path. 

## <a name="Running_Tests"></a>4. Running Tests
Provided your PYTHONPATH was set correctly, you can run the tests from your `<clone_root>` directory.

1. Run all tests:
    ##### Windows

    ```BatchFile
    <clone_root>\run_all_tests.bat
    ```
    ##### MacOS/Linux (bash)
    ```Shell
    . <clone_root>/run_all_tests.sh
    ```
2. Running tests for specific components:
  
    To test the mssqlscripter:
    ```BatchFile
    python -m unittest discover -s mssqlscripter/tests
    ```
    To test the jsonrpc library:
    ```BatchFile
    python -m unittest discover -s mssqlscripter/jsonrpc/tests
    ```

    To test the scripting service:
    ```BatchFile
    python -m unittest discover -s mssqlscripter/jsonrpc/contracts/tests
    ```

## <a name="Run_mssql-scripter"></a>5. Running mssql-scripter
#### Command line

1.  Invoke mssql-scripter using:

    ##### MacOS/Linux (bash):
    ```Shell
    mssql-scripter -h
    ```

    ##### Windows:
    ```BatchFile
    <clone_root>\mssql-scripter.bat -h
    ```
    which is equivalent to the following:
    ```BatchFile
    python -m mssqlscripter -h
    ```
