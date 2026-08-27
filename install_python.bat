@echo off
REM Python 3.11 Installation Script

setlocal enabledelayedexpansion

echo.
echo ========================================
echo Python 3.11.9 Installation Script
echo ========================================
echo.

REM Check if Python is installed
echo [1/4] Checking if Python is already installed...
python --version >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo.
    python --version
    echo [OK] Python is already installed!
    echo.
    goto end
)

REM Download Python installer
echo [2/4] Downloading Python 3.11.9 installer (25 MB)...
set INSTALLER=%TEMP%\python-3.11.9-amd64.exe
powershell -NoProfile -Command "$ProgressPreference='SilentlyContinue'; Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe' -OutFile '%INSTALLER%' -UseBasicParsing" >nul 2>&1

if not exist "%INSTALLER%" (
    echo [X] Failed to download Python installer
    pause
    exit /b 1
)
echo [OK] Downloaded to: %INSTALLER%
echo.

REM Install Python (all-users needs admin; fall back to per-user install)
echo [3/4] Installing Python (this may take 1-2 minutes)...
net session >nul 2>&1
if %ERRORLEVEL% equ 0 (
    "%INSTALLER%" /quiet InstallAllUsers=1 PrependPath=1 Include_pip=1 Include_tcltk=1 Include_dev=1
) else (
    echo Not running as administrator - installing for current user only
    "%INSTALLER%" /quiet InstallAllUsers=0 PrependPath=1 Include_pip=1 Include_tcltk=1 Include_dev=1
)
if %ERRORLEVEL% neq 0 (
    echo [X] Installation failed
    pause
    exit /b 1
)
echo [OK] Installation completed
echo.

REM Verify installation. PATH changes don't reach this already-running shell,
REM so check the known install locations directly.
echo [4/4] Verifying installation...
ping -n 4 127.0.0.1 >nul
set PY_EXE=
if exist "C:\Program Files\Python311\python.exe" set "PY_EXE=C:\Program Files\Python311\python.exe"
if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" set "PY_EXE=%LOCALAPPDATA%\Programs\Python\Python311\python.exe"

if defined PY_EXE (
    echo.
    "%PY_EXE%" --version
    echo [OK] Python is installed!
    echo.
    echo ========================================
    echo Installation Complete!
    echo ========================================
    echo.
    echo Next steps (in a NEW terminal, so PATH is refreshed):
    echo 1. cd "%~dp0"
    echo 2. python -m venv venv
    echo 3. venv\Scripts\activate
    echo 4. pip install -r requirements.txt
    echo.
) else (
    echo [X] Python verification failed
    echo Try opening a new terminal and running: python --version
)

:end
if defined INSTALLER del /f /q "%INSTALLER%" 2>nul
pause
