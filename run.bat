@echo off
REM Sports Events Scraper - manual run
REM Double-click this file to run the scraper and watch the output live.
REM You can scrape everything, or enter one specific link to scrape.

setlocal
cd /d "%~dp0"

set PYTHON_PATH=%~dp0venv\Scripts\python.exe
if not exist "%PYTHON_PATH%" (
    echo NOTE: virtual environment not found - using system Python.
    echo       If this fails, run complete_setup.bat first.
    set PYTHON_PATH=python
)

set TARGET_URL=
set SPORT_NAME=
set /p TARGET_URL=Enter a link to scrape (or press Enter to scrape all configured sources):
if "%TARGET_URL%"=="" goto run_all

set /p SPORT_NAME=Sport for this link (or press Enter to auto-detect):
echo.
echo Scraping %TARGET_URL% ...
echo.
if "%SPORT_NAME%"=="" goto run_url_nosport
"%PYTHON_PATH%" main.py --url "%TARGET_URL%" --sport "%SPORT_NAME%"
set EXITCODE=%ERRORLEVEL%
goto done

:run_url_nosport
"%PYTHON_PATH%" main.py --url "%TARGET_URL%"
set EXITCODE=%ERRORLEVEL%
goto done

:run_all
echo.
echo Running the scraper - this takes a few minutes...
echo.
"%PYTHON_PATH%" main.py
set EXITCODE=%ERRORLEVEL%

:done
echo.
if %EXITCODE% equ 0 (
    echo Done! Results are in output\sports_events_[timestamp].xlsx
) else (
    echo The scraper reported a problem - check logs\scraper.log
)
echo.
pause
exit /b %EXITCODE%
