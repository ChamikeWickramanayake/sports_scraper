@echo off
REM Sports Events Scraper - Windows Task Scheduler Wrapper
REM This script is called by Windows Task Scheduler to run the daily scraper

REM Set paths
set SCRIPT_DIR=%~dp0
set PYTHON_PATH=%SCRIPT_DIR%venv\Scripts\python.exe
set MAIN_SCRIPT=%SCRIPT_DIR%main.py
set LOG_DIR=%SCRIPT_DIR%logs

REM Create logs directory if it doesn't exist
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

REM Set timestamp for logging
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate=%%c-%%a-%%b)
for /f "tokens=1-2 delims=/:" %%a in ('time /t') do (set mytime=%%a%%b)
set TIMESTAMP=%mydate%_%mytime%

REM Log file
set LOG_FILE=%LOG_DIR%\scheduler_%TIMESTAMP%.log

REM Run the scraper
echo. >> "%LOG_FILE%"
echo ====== Sports Events Scraper Run ====== >> "%LOG_FILE%"
echo Start Time: %date% %time% >> "%LOG_FILE%"
echo. >> "%LOG_FILE%"

REM Activate virtual environment and run main script
cd /d "%SCRIPT_DIR%"
call "%PYTHON_PATH%" "%MAIN_SCRIPT%" >> "%LOG_FILE%" 2>&1

REM Log completion
echo. >> "%LOG_FILE%"
echo End Time: %date% %time% >> "%LOG_FILE%"
echo ======================================== >> "%LOG_FILE%"

REM Exit with appropriate code
if %ERRORLEVEL% equ 0 (
    echo Scraper completed successfully. >> "%LOG_FILE%"
    exit /b 0
) else (
    echo Scraper failed with error code %ERRORLEVEL%. >> "%LOG_FILE%"
    exit /b %ERRORLEVEL%
)
