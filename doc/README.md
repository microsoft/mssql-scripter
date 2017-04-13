Setting up your development environment
========================================
1.  Add `<clone root>` to your PYTHONPATH environment variable:
  
  ##### Windows
  ```BatchFile
  set PYTHONPATH=<clone root>;%PYTHONPATH%
  ```
  
  ##### OSX/Ubuntu (bash)
  ```Shell
  export PYTHONPATH=<clone root>:${PYTHONPATH}
  ```
  
2.	Install the dependencies via pip with the script below.
  ```Shell
  python dev_setup.py
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

