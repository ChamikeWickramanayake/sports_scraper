@echo off
REM Python 3.11 Installation Script

echo.
echo ========================================
echo Python 3.11.9 Installation Script
echo ========================================
echo.

REM Check if Python is installed
echo [1/4] Checking if Python is already installed...
python --version >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo.
    python --version
    echo ✓ Python is already installed!
    echo.
    goto end
)

REM Download Python installer
echo [2/4] Downloading Python 3.11.9 installer (25 MB)...
set INSTALLER=%TEMP%\python-3.11.9-amd64.exe
powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe' -OutFile '%INSTALLER%' -UseBasicParsing" >nul 2>&1

if not exist "%INSTALLER%" (
    echo ✗ Failed to download Python installer
    pause
    exit /b 1
)
echo ✓ Downloaded to: %INSTALLER%
echo.

REM Install Python
echo [3/4] Installing Python (this may take 1-2 minutes)...
"%INSTALLER%" /quiet InstallAllUsers=1 PrependPath=1 Include_pip=1 Include_tcltk=1 Include_dev=1
if %ERRORLEVEL% neq 0 (
    echo ✗ Installation failed
    pause
    exit /b 1
)
echo ✓ Installation completed
echo.

REM Verify installation
echo [4/4] Verifying installation...
timeout /t 3 /nobreak >nul
python --version >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo.
    python --version
    echo ✓ Python is ready!
    echo.
    echo ========================================
    echo Installation Complete!
    echo ========================================
    echo.
    echo Next steps:
    echo 1. Open a new Command Prompt or PowerShell
    echo 2. cd "e:\PEO SPORTS\sports_scraper"
    echo 3. python -m venv venv
    echo 4. venv\Scripts\activate
    echo 5. pip install -r requirements.txt
    echo.
) else (
    echo ✗ Python verification failed
    echo Try opening a new terminal and running: python --version
)

:end
del /f /q "%INSTALLER%" 2>nul
pause
