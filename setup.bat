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
if exist "venv" (
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

echo [3/4] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)
echo Virtual environment activated
echo.

echo [4/4] Installing dependencies...
pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt
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
echo 1. Download credentials.json from Google Cloud Console
echo 2. Place it in: config/credentials.json
echo 3. Set environment variable: GOOGLE_SHEET_ID=your-sheet-id
echo 4. Run: python main.py
echo.
echo For detailed setup instructions, see README.md
echo.

pause
