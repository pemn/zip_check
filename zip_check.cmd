::!cmd
@echo off
setlocal
:: Search for the latest python distribution
if defined WINPYDIRBASE goto PYTHON_OK
for /d %%i in (%appdata%\WPy64*) do set WINPYDIRBASE=%%i
if not defined WINPYDIRBASE (
    echo.
    echo Python runtime not found. 
    echo Download Winpython and extract to APPDATA system folder:
    echo %APPDATA%
    echo.
    pause
    goto :EOF
)
call "%WINPYDIRBASE%\scripts\env.bat"
:PYTHON_OK
python -V
set python_cmd="%~dpn0.py"
if not exist %python_cmd% (
    set python_cmd=-m _gui "%~f0"
)
python %python_cmd%
if errorlevel 1 pause
