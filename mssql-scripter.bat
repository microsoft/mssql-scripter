@echo off
setlocal
REM Set the python io encoding to UTF-8 by default if not set.
IF "%PYTHONIOENCODING%"=="" (
    SET PYTHONIOENCODING="UTF-8"
    REM Used as a flag to tell scripter we manually set the encoding.
    SET MSSQLSCRIPTER_DEFAULT_ENCODING="TRUE"
)
SET PYTHONPATH=%~dp0;%PYTHONPATH%
python -m mssqlscripter %*

endlocal
