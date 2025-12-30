@echo off
:: Check for admin privileges
NET SESSION >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Requesting administrative privileges...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

:: Set the path to python and your script
set PYTHON_PATH=C:\Path\To\Python\python.exe
set SCRIPT_PATH="D:\Cybersecurity-Log-Analyser\src\system_log.py"

:: Run the script
"%PYTHON_PATH%" "%SCRIPT_PATH%"

pause
