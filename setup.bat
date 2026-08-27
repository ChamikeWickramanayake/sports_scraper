@echo off
REM Setup Script for Sports Events Scraper
REM Automates virtual environment creation and dependency installation

setlocal enabledelayedexpansion

echo.
echo ===============================================
echo Sports Events Scraper - Setup Script
echo ===============================================
echo.

REM Get current directory
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

echo [1/4] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.8+ and add to PATH.
    pause
    exit /b 1
)
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Found Python %PYTHON_VERSION%
echo.

echo [2/4] Creating virtual environment...
if exist "venv\Scripts\python.exe" (
    echo Virtual environment already exists. Skipping...
) else (
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created successfully
)
echo.

echo [3/4] Verifying virtual environment...
set VENV_PY=%SCRIPT_DIR%venv\Scripts\python.exe
if not exist "%VENV_PY%" (
    echo ERROR: Virtual environment is incomplete - delete the venv folder and re-run
    pause
    exit /b 1
)
echo Virtual environment ready
echo.

echo [4/4] Installing dependencies...
"%VENV_PY%" -m pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo Dependencies installed successfully
echo.

echo ===============================================
echo Setup completed successfully!
echo ===============================================
echo.
echo Next steps:
echo 1. Run the scraper:  venv\Scripts\python.exe main.py
echo 2. Check the output: output\sports_events_[timestamp].xlsx
echo 3. Check the logs:   logs\scraper.log
echo.
echo For detailed setup instructions, see README.md
echo.

pause
