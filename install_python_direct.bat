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
powershell -NoProfile -Command "$ProgressPreference = 'SilentlyContinue'; Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe' -OutFile '%TEMP%\python-install.exe' -UseBasicParsing"

if not exist "%TEMP%\python-install.exe" (
    echo ERROR: Failed to download Python
    pause
    exit /b 1
)
echo [OK] Downloaded

echo.
echo [2/3] Running installer...
REM All-users install needs admin; fall back to per-user install
net session >nul 2>&1
if %ERRORLEVEL% equ 0 (
    "%TEMP%\python-install.exe" /quiet InstallAllUsers=1 PrependPath=1 Include_pip=1
) else (
    echo Not running as administrator - installing for current user only
    "%TEMP%\python-install.exe" /quiet InstallAllUsers=0 PrependPath=1 Include_pip=1
)
if %ERRORLEVEL% neq 0 (
    echo WARNING: Installer returned error code %ERRORLEVEL%
)

ping -n 6 127.0.0.1 >nul

echo.
echo [3/3] Verifying installation...
REM PATH changes don't reach this already-running shell,
REM so check the known install locations directly.
set PY_EXE=
if exist "C:\Program Files\Python311\python.exe" set "PY_EXE=C:\Program Files\Python311\python.exe"
if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" set "PY_EXE=%LOCALAPPDATA%\Programs\Python\Python311\python.exe"

if defined PY_EXE (
    for /f "tokens=2" %%i in ('"!PY_EXE!" --version 2^>^&1') do set PYTHON_VERSION=%%i
    echo [OK] Python !PYTHON_VERSION! installed successfully!
    echo Open a NEW terminal so the updated PATH takes effect, then run: python --version
) else (
    python --version >nul 2>&1
    if !ERRORLEVEL! equ 0 (
        for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
        echo [OK] Python !PYTHON_VERSION! is available
    ) else (
        echo [X] Installation failed - Python not found
        pause
        exit /b 1
    )
)

del /f "%TEMP%\python-install.exe" 2>nul
echo.
echo Complete!
pause
