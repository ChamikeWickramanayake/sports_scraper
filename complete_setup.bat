@echo off
REM ========================================
REM  Sports Events Scraper - Complete Setup
REM ========================================

setlocal enabledelayedexpansion

echo.
echo ========================================
echo Sports Events Scraper - Complete Setup
echo ========================================
echo.

REM Get current directory
cd /d "%~dp0"
set SCRIPT_DIR=%CD%

echo [Step 1/5] Checking Python...
python --version >nul 2>&1
if %ERRORLEVEL% equ 0 (
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
    echo [OK] Found Python !PYTHON_VERSION!
) else (
    echo [X] Python not found! Please install Python 3.8+ first.
    echo Visit: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation!
    echo.
    pause
    exit /b 1
)

echo.
echo [Step 2/5] Creating virtual environment...
if exist "%SCRIPT_DIR%\venv\Scripts\python.exe" (
    echo [OK] Virtual environment already exists
) else (
    python -m venv venv
    if !ERRORLEVEL! neq 0 (
        echo [X] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
)

echo.
echo [Step 3/5] Verifying virtual environment...
set VENV_PY=%SCRIPT_DIR%\venv\Scripts\python.exe
if not exist "%VENV_PY%" (
    echo [X] Virtual environment is incomplete - delete the venv folder and re-run
    pause
    exit /b 1
)
echo [OK] Virtual environment ready

echo.
echo [Step 4/5] Installing dependencies...
echo This may take 2-3 minutes...
"%VENV_PY%" -m pip install -r requirements.txt
if %ERRORLEVEL% neq 0 (
    echo [X] Failed to install dependencies
    pause
    exit /b 1
)
echo [OK] Dependencies installed successfully

echo.
echo [Step 5/5] Testing setup...
"%VENV_PY%" test_scrapers.py
if %ERRORLEVEL% neq 0 (
    echo [!] Setup test reported problems - check logs\scraper.log for details
    pause
    exit /b 1
)
echo [OK] Setup test completed

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Run the scraper:
echo    - venv\Scripts\python.exe main.py
echo.
echo 2. Check the output:
echo    - Excel file: output\sports_events.xlsx
echo    - Log file: logs\scraper.log
echo.
echo For full documentation, see README.md or QUICKSTART.md
echo.
pause
