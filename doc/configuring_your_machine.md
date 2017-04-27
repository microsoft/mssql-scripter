Setting up your development environment
========================================
The mssql-scripter projects sources are located on GitHub (https://github.com/Microsoft/sql-xplat-cli/). In order to contribute to the project, you are expected to: 
-	Have a GitHub account. For Microsoft contributors, follow the guidelines on https://opensourcehub.microsoft.com/ to create, configure and link your account
-	Fork the  https://github.com/Microsoft/sql-xplat-cli/ repository into your private GitHub account
-	Create pull requests against the https://github.com/Microsoft/sql-xplat-cli/ repository to get your code changes merged into the project repository.

## Preparing your machine
1.	Install Python 3.5.x from http://python.org. Please note that the version of Python that comes preinstalled on OSX is 2.7. 
2.	Clone your repository and check out the master branch.
3.	Create a new virtual environment “env” for Python 3.5 in the root of your clone. You can do this by running:

  ##### Windows
  ```BatchFile
  python -m venv <clone root>\env
  ```
  ##### OSX/Ubuntu (bash)
  ```Shell
  python –m venv <clone root>/env
  ```
4.  Activate the env virtual environment by running:

  ##### Windows
  ```BatchFile
  <clone root>\env\scripts\activate.bat
  ```
  ##### OSX/Ubuntu (bash)
  ```Shell
  sh <clone root>/env/bin/activate
  ```

5.	Install the dependencies using pip.
  ```Shell
  python <clone root>/dev_setup.py clean
  ```
6.  Add `<clone root>` to your PYTHONPATH environment variable:

  ##### Windows
  ```BatchFile
  set PYTHONPATH=<clone root>;%PYTHONPATH%
  ```
  ##### OSX/Ubuntu (bash)
  ```Shell
  export PYTHONPATH=<clone root>:${PYTHONPATH}
  ```


## Configuring your IDE
#### Visual Studio (Windows only)
1.	Install Python Tools for Visual Studio. As of 2/18/2016, the current version (PTVS 2.2) can be found at http://microsoft.github.io/PTVS/.
2.	Open the sql-xplat-cli.pyproj project
You should now be able to launch your project by pressing F5/start debugging

#### Visual Studio Code (Any platform)
Experimental steps – still haven’t been able to get virtual environments to work well with VSCode

1.	Install VS Code
2.	Install (one of) the python extension(s) (https://marketplace.visualstudio.com/items?itemName=donjayamanne.python)
Debugging should now work (including stepping and setting breakpoints). 


## Running CLI
#### Command line
1.  Activate your virtual environment if not already done

  ##### OSX/Ubuntu (bash):
  ```Shell
  source <clone root>/env/bin/activate
  ```

  ##### Windows:
  ```BatchFile
  <clone root>\env\scripts\activate.bat
  ```

2.  Invoke the CLI using:

  ##### OSX/Ubuntu (bash):
  ```Shell
  mssql-scripter
  ```

  ##### Windows:
  ```BatchFile
  <clone root>\mssql-scripter.bat 
  ```
  which is equivalent to the following:
  ```BatchFile
  python -m mssqlscripter 
  ```

## Running Tests:
#### Command line
  Provided your PYTHONPATH was set correctly, you can run the tests from your `<root clone>` directory.

  To test the jsonrpc modules of the CLI:
  ```BatchFile
  python -m unittest discover -s mssqlscripter/jsonrpc/tests
  python -m unittest discover -s mssqlscripter/jsonrpc/contracts/tests
  ```
 
  To test the scripter module of the CLI:
  ```BatchFile
  python -m unittest discover -s mssqlscripter/tests
  ```

  Additionally, you can run tests for all CLI tools and common modules using the `run_all_tests.bat` or `sh run_all_tests` script.

#### VS Code
  Under construction...
  
#### Visual Studio
 Under construction...
