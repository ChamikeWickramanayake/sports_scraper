@echo off
REM Python Installation with GUI
REM This will show the Python installer graphically so we can see any errors

echo.
echo ========================================
echo Python 3.11.9 Installation (GUI Mode)
echo ========================================
echo.
echo Starting the Python installer...
echo If the installer doesn't appear, check if it opens in the background.
echo.

set INSTALLER="%TEMP%\python-3.11.9-amd64.exe"

if not exist %INSTALLER% (
    echo Downloading Python installer...
    powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe' -OutFile %INSTALLER% -UseBasicParsing"
)

echo Running installer (GUI mode)...
echo.
echo IMPORTANT:
echo - CHECK "Add Python to PATH"
echo - Click "Install Now"
echo - Wait for completion
echo.

%INSTALLER%

echo.
echo Installation complete. Checking Python...
timeout /t 3
python --version

if %ERRORLEVEL% equ 0 (
    echo SUCCESS: Python is installed!
) else (
    echo ERROR: Python command not found
    echo Try closing and reopening your terminal
)

pause
