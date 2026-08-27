@echo off
REM Sports Events Scraper - Windows Task Scheduler Wrapper
REM This script is called by Windows Task Scheduler to run the daily scraper

setlocal

REM Set paths
set SCRIPT_DIR=%~dp0
set PYTHON_PATH=%SCRIPT_DIR%venv\Scripts\python.exe
set MAIN_SCRIPT=%SCRIPT_DIR%main.py
set LOG_DIR=%SCRIPT_DIR%logs

REM Create logs directory if it doesn't exist
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

REM Fall back to system Python if the virtual environment doesn't exist
set VENV_NOTE=
if not exist "%PYTHON_PATH%" (
    set PYTHON_PATH=python
    set VENV_NOTE=NOTE: venv\Scripts\python.exe not found - using system Python
)

REM Locale-independent timestamp for the log filename
for /f %%i in ('powershell -NoProfile -Command "Get-Date -Format yyyy-MM-dd_HHmm"') do set TIMESTAMP=%%i
if not defined TIMESTAMP set TIMESTAMP=run

REM Log file
set LOG_FILE=%LOG_DIR%\scheduler_%TIMESTAMP%.log

REM Run the scraper
echo. >> "%LOG_FILE%"
echo ====== Sports Events Scraper Run ====== >> "%LOG_FILE%"
echo Start Time: %date% %time% >> "%LOG_FILE%"
if defined VENV_NOTE echo %VENV_NOTE% >> "%LOG_FILE%"
echo. >> "%LOG_FILE%"

cd /d "%SCRIPT_DIR%"
"%PYTHON_PATH%" "%MAIN_SCRIPT%" >> "%LOG_FILE%" 2>&1
set EXITCODE=%ERRORLEVEL%

REM Log completion
echo. >> "%LOG_FILE%"
echo End Time: %date% %time% >> "%LOG_FILE%"
echo ======================================== >> "%LOG_FILE%"

REM Exit with the scraper's code
if %EXITCODE% equ 0 (
    echo Scraper completed successfully. >> "%LOG_FILE%"
) else (
    echo Scraper failed with error code %EXITCODE%. >> "%LOG_FILE%"
)
exit /b %EXITCODE%
