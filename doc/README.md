Setting up your development environment
========================================
1.	Install the dependencies via pip with the script below.
  ```Shell
  python scripts/dev_setup.py
  ```
2.  Add `<clone root>\src` to your PYTHONPATH environment variable:
  
  ##### Windows
  ```BatchFile
  set PYTHONPATH=<clone root>\mssql-scripter;%PYTHONPATH%
  ```
  
  ##### OSX/Ubuntu (bash)
  ```Shell
  export PYTHONPATH=<clone root>/mssql-scripter:${PYTHONPATH}
  ```
## Running Tests:
#### Command line
  Provided your PYTHONPATH was set correctly, you can run the tests from your `<root clone>` directory.

  To test the common modules of the CLI:
  ```BatchFile
  python -m unittest discover -s mssql-scripter/mssql/common/tests
  ```
 
  To test the scripter module of the CLI:
  ```BatchFile
  python -m unittest discover -s mssql-scripter/mssql/scripter/tests
  ```

  Additionally, you can run tests for all CLI tools and common modules using the `run_all_tests.bat` or `sh run_all_tests` script.
