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

set INSTALLER=%TEMP%\python-3.11.9-amd64.exe

if not exist "%INSTALLER%" (
    echo Downloading Python installer...
    powershell -NoProfile -Command "$ProgressPreference='SilentlyContinue'; Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe' -OutFile '%INSTALLER%' -UseBasicParsing"
)

if not exist "%INSTALLER%" (
    echo ERROR: Failed to download the installer
    pause
    exit /b 1
)

echo Running installer (GUI mode)...
echo.
echo IMPORTANT:
echo - CHECK "Add Python to PATH"
echo - Click "Install Now"
echo - Wait for completion
echo.

start /wait "" "%INSTALLER%"

echo.
echo Installation complete. Checking Python...
echo (PATH changes only reach NEW terminals - this check may fail even
echo  after a successful install.)
python --version
if %ERRORLEVEL% equ 0 (
    echo SUCCESS: Python is installed!
) else (
    echo Python not found in this session's PATH.
    echo Close and reopen your terminal, then run: python --version
)

pause
