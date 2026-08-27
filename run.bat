@echo off
REM Sports Events Scraper - manual run
REM Double-click this file to run the scraper and watch the output live.

setlocal
cd /d "%~dp0"

set PYTHON_PATH=%~dp0venv\Scripts\python.exe
if not exist "%PYTHON_PATH%" (
    echo NOTE: virtual environment not found - using system Python.
    echo       If this fails, run complete_setup.bat first.
    set PYTHON_PATH=python
)

echo Running the scraper - this takes a few minutes...
echo.
"%PYTHON_PATH%" main.py
set EXITCODE=%ERRORLEVEL%

echo.
if %EXITCODE% equ 0 (
    echo Done! Results are in output\sports_events.xlsx
) else (
    echo The scraper reported a problem - check logs\scraper.log
)
echo.
pause
exit /b %EXITCODE%
