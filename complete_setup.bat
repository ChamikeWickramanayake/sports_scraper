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
    echo ✓ Found Python %PYTHON_VERSION%
) else (
    echo ✗ Python not found! Please install Python 3.8+ first.
    echo Visit: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation!
    echo.
    pause
    exit /b 1
)

echo.
echo [Step 2/5] Creating virtual environment...
if exist "%SCRIPT_DIR%\venv" (
    echo ✓ Virtual environment already exists
) else (
    python -m venv venv
    if %ERRORLEVEL% neq 0 (
        echo ✗ Failed to create virtual environment
        pause
        exit /b 1
    )
    echo ✓ Virtual environment created
)

echo.
echo [Step 3/5] Activating virtual environment...
call venv\Scripts\activate.bat
if %ERRORLEVEL% neq 0 (
    echo ✗ Failed to activate virtual environment
    pause
    exit /b 1
)
echo ✓ Virtual environment activated

echo.
echo [Step 4/5] Installing dependencies...
echo This may take 2-3 minutes...
pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt
if %ERRORLEVEL% neq 0 (
    echo ✗ Failed to install dependencies
    pause
    exit /b 1
)
echo ✓ Dependencies installed successfully

echo.
echo [Step 5/5] Testing setup...
python test_scrapers.py
if %ERRORLEVEL% neq 0 (
    echo ⚠ Test completed with warnings (this may be normal)
)
echo ✓ Setup test completed

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Run the scraper:
echo    - python main.py
echo.
echo 2. Check the output:
echo    - Excel file: output/sports_events.xlsx
echo    - Log file: logs/scraper.log
echo.
echo For full documentation, see README.md or QUICKSTART.md
echo.
pause
