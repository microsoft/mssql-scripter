@echo off
setlocal

SET PYTHONPATH=%~dp0;%PYTHONPATH%
python -m mssqlscripter %*

endlocal
