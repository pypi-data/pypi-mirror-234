@echo off

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% == 0 (
    echo Python is already installed
) else (
    REM Download and install Python
    echo Python is not installed, downloading and installing...
    powershell.exe -Command "Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe -OutFile %TEMP%\python-3.10.0-amd64.exe"
    %TEMP%\python-3.10.0-amd64.exe /quiet InstallAllUsers=1 PrependPath=1
    echo Python installed successfully
)

REM Load a Python file
set "file_path=Task.py"
if exist "%file_path%" (
    python "%file_path%"
) else (
    echo File not found: %file_path%
)
