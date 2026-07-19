@echo off
REM Direct Python Installation Script
REM Downloads from python.org and installs locally

setlocal enabledelayedexpansion

echo.
echo ========================================
echo Python 3.11.9 Installation
echo ========================================
echo.

cd /d "%~dp0"

echo [1/3] Downloading Python installer...
powershell -Command "$ProgressPreference = 'SilentlyContinue'; Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe' -OutFile '%TEMP%\python-install.exe'" 

if not exist "%TEMP%\python-install.exe" (
    echo ERROR: Failed to download Python
    timeout /t 5
    exit /b 1
)
echo ✓ Downloaded

echo.
echo [2/3] Running installer (InstallAllUsers=1 PrependPath=1)...
"%TEMP%\python-install.exe" /quiet InstallAllUsers=1 PrependPath=1 Include_pip=1

if %ERRORLEVEL% neq 0 (
    echo WARNING: Installer returned error code %ERRORLEVEL%
    echo Attempting alternative installation method...
)

timeout /t 5

echo.
echo [3/3] Verifying installation...
python --version >nul 2>&1
if %ERRORLEVEL% equ 0 (
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
    echo ✓ Python %PYTHON_VERSION% installed successfully!
) else (
    echo ✗ Python not found in PATH
    echo Checking installation directory...
    
    dir "C:\Program Files\Python311\python.exe" 2>nul
    if %ERRORLEVEL% equ 0 (
        echo ✓ Python installed but not in PATH
        echo Adding to PATH...
        setx PATH "%PATH%;C:\Program Files\Python311"
        echo Please restart your terminal and try again
    ) else (
        echo ✗ Installation failed
        timeout /t 5
        exit /b 1
    )
)

del /f "%TEMP%\python-install.exe" 2>nul
echo.
echo Complete!
