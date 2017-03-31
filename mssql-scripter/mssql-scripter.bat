@echo off
setlocal

SET PYTHONPATH=%~dp0/src;%PYTHONPATH%
python -m mssql.scripter %*

endlocal