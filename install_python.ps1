# Python 3.11 Installation Script for Windows
# Downloads and installs Python with PATH integration
# Run with: powershell -ExecutionPolicy Bypass -File install_python.ps1

$pythonUrl = "https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe"
$installerPath = "$env:TEMP\python-3.11.9-amd64.exe"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Python 3.11.9 Installation Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if already installed (Get-Command avoids stale $LASTEXITCODE and the
# Microsoft Store python.exe alias stub)
Write-Host "[1/4] Checking if Python is already installed..." -ForegroundColor Yellow
$existing = Get-Command python -ErrorAction SilentlyContinue
if ($existing -and $existing.Source -notmatch "WindowsApps") {
    $pythonVersion = & python --version 2>&1
    Write-Host "[OK] Python is already installed: $pythonVersion" -ForegroundColor Green
    exit 0
}
Write-Host "Python not found, proceeding with installation..." -ForegroundColor Yellow

# Download installer
Write-Host "[2/4] Downloading Python 3.11.9 installer (25 MB)..." -ForegroundColor Yellow
try {
    $ProgressPreference = 'SilentlyContinue'
    Invoke-WebRequest -Uri $pythonUrl -OutFile $installerPath -UseBasicParsing
    Write-Host "[OK] Downloaded to: $installerPath" -ForegroundColor Green
}
catch {
    Write-Host "[X] Failed to download: $_" -ForegroundColor Red
    exit 1
}

# Install Python (all-users needs admin; fall back to a per-user install)
Write-Host "[3/4] Installing Python (this may take 1-2 minutes)..." -ForegroundColor Yellow
$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if ($isAdmin) {
    $installArgs = "/quiet InstallAllUsers=1 PrependPath=1 Include_pip=1 Include_tcltk=1 Include_dev=1"
}
else {
    Write-Host "Not running as administrator - installing for current user only" -ForegroundColor Yellow
    $installArgs = "/quiet InstallAllUsers=0 PrependPath=1 Include_pip=1 Include_tcltk=1 Include_dev=1"
}
try {
    $process = Start-Process -FilePath $installerPath -ArgumentList $installArgs -Wait -PassThru

    if ($process.ExitCode -eq 0) {
        Write-Host "[OK] Installation successful" -ForegroundColor Green
    }
    else {
        Write-Host "[X] Installation failed with exit code: $($process.ExitCode)" -ForegroundColor Red
        exit 1
    }
}
catch {
    Write-Host "[X] Error during installation: $_" -ForegroundColor Red
    exit 1
}

# Verify installation
Write-Host "[4/4] Verifying installation..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

# Refresh environment variables
$env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User")

$installed = Get-Command python -ErrorAction SilentlyContinue
if ($installed -and $installed.Source -notmatch "WindowsApps") {
    $pythonVersion = & python --version 2>&1
    Write-Host "[OK] Python is ready: $pythonVersion" -ForegroundColor Green
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "Installation Complete!" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "1. cd '$PSScriptRoot'" -ForegroundColor White
    Write-Host "2. python -m venv venv" -ForegroundColor White
    Write-Host "3. venv\Scripts\activate" -ForegroundColor White
    Write-Host "4. pip install -r requirements.txt" -ForegroundColor White
    Write-Host ""
}
else {
    Write-Host "[X] Python verification failed" -ForegroundColor Red
    Write-Host "Try opening a new terminal and running: python --version" -ForegroundColor Yellow
    exit 1
}

# Cleanup
Remove-Item -Force -ErrorAction SilentlyContinue $installerPath
Write-Host "Cleanup completed." -ForegroundColor Gray
