Setting up your Development Environment
========================================
mssql-scripter sources are located on GitHub (https://github.com/Microsoft/sql-xplat-cli). In order to contribute to the project, you are expected to: 
-	Have a GitHub account. For Microsoft contributors, follow the guidelines on https://opensourcehub.microsoft.com/ to create, configure and link your account
-	Fork the  https://github.com/Microsoft/sql-xplat-clirepository into your private GitHub account
-	Create pull requests against the https://github.com/Microsoft/sql-xplat-cli repository to get your code changes merged into the project repository.

## Preparing your machine
1.	Install latest Python from http://python.org. Please note that the version of Python that comes preinstalled on OSX is 2.7. 
    #### Windows
    - Install latest Python from [here](http://python.org).
    - During installation, check the 'Add Python X.Y to PATH' option.
    
2. Clone the repo from [https://github.com/Microsoft/sql-xplat-cli](https://github.com/Microsoft/sql-xplat-cli)
3. If not developing in a virtual environment, proceed to [Development Setup](#Development).

### Virtual Environment setup
1. Create a virtual environment in a subdirectory of your `<clone root>`, using `<clone root>/env` as a example:
 
     ##### Windows
    ```BatchFile
    python -m venv <clone root>\env
    ```
    ##### OSX/Ubuntu (bash)
    ```Shell
    python –m venv <clone root>/env
    ```
2.  Activate the env virtual environment by running:

    ##### Windows
    ```BatchFile
    <clone root>\env\scripts\activate.bat
    ```
    ##### OSX/Ubuntu (bash)
    ```Shell
    . <clone root>/env/bin/activate
    ```
3. To deactivate the virtual environment:

    ##### Windows
    ```BatchFile
    <clone root>\env\scripts\deactivate.bat
    ```
    ##### OSX/Ubuntu (bash)
    ```Shell
    deactivate
    ```
### <a name="Development"></a>Development Setup
1.  Add `<clone root>` to your PYTHONPATH environment variable:

    ##### Windows
    ```BatchFile
    set PYTHONPATH=<clone root>;%PYTHONPATH%
    ```
    ##### OSX/Ubuntu (bash)
    ```Shell
    export PYTHONPATH=<clone root>:${PYTHONPATH}
    ```
2.	Install the dependencies:
    ```Shell
    python <clone root>/dev_setup.py
    ```

## Running Tests
Provided your PYTHONPATH was set correctly, you can run the tests from your `<root clone>` directory.

1. Run all tests:
    ##### Windows

    ```BatchFile
    <clone root>\run_all_tests.bat
    ```
    ##### OSX/Ubuntu (bash)
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
## Configuring your IDE
#### Visual Studio (Windows only)
1.	Install Python Tools for Visual Studio. As of 2/18/2016, the current version (PTVS 2.2) can be found at http://microsoft.github.io/PTVS/.
2.	Open the sql-xplat-cli.pyproj project
You should now be able to launch your project by pressing F5/start debugging

#### Visual Studio Code (Any platform)

1.	Install VS Code
2.	Install (one of) the python extension(s) (https://marketplace.visualstudio.com/items?itemName=donjayamanne.python)
Debugging should now work (including stepping and setting breakpoints). 

The repo has a launch.json file that will launch the version of Python that is first on your path. 

## Running mssql-scripter
#### Command line

1.  Invoke mssql-scripter using:

    ##### OSX/Ubuntu (bash):
    ```Shell
    mssql-scripter -h
    ```

    ##### Windows:
    ```BatchFile
    <clone root>\mssql-scripter.bat -h
    ```
    which is equivalent to the following:
    ```BatchFile
    python -m mssqlscripter -h
    ```
