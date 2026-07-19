# Python 3.11 Installation Script for Windows
# Downloads and installs Python with PATH integration

$pythonUrl = "https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe"
$installerPath = "$env:TEMP\python-3.11.9-amd64.exe"
$logPath = "$env:TEMP\python-install.log"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Python 3.11.9 Installation Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if already installed
Write-Host "[1/4] Checking if Python is already installed..." -ForegroundColor Yellow
try {
    $pythonVersion = & python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Python is already installed: $pythonVersion" -ForegroundColor Green
        exit 0
    }
}
catch {
    Write-Host "Python not found, proceeding with installation..." -ForegroundColor Yellow
}

# Download installer
Write-Host "[2/4] Downloading Python 3.11.9 installer (25 MB)..." -ForegroundColor Yellow
try {
    $ProgressPreference = 'SilentlyContinue'
    Invoke-WebRequest -Uri $pythonUrl -OutFile $installerPath -UseBasicParsing
    Write-Host "✓ Downloaded to: $installerPath" -ForegroundColor Green
}
catch {
    Write-Host "✗ Failed to download: $_" -ForegroundColor Red
    exit 1
}

# Install Python
Write-Host "[3/4] Installing Python (this may take 1-2 minutes)..." -ForegroundColor Yellow
try {
    $process = Start-Process -FilePath $installerPath `
        -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1 Include_pip=1 Include_tcltk=1 Include_dev=1" `
        -Wait -PassThru
    
    if ($process.ExitCode -eq 0) {
        Write-Host "✓ Installation successful" -ForegroundColor Green
    }
    else {
        Write-Host "✗ Installation failed with exit code: $($process.ExitCode)" -ForegroundColor Red
        exit 1
    }
}
catch {
    Write-Host "✗ Error during installation: $_" -ForegroundColor Red
    exit 1
}

# Verify installation
Write-Host "[4/4] Verifying installation..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

# Refresh environment variables
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

try {
    $pythonVersion = & python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Python is ready: $pythonVersion" -ForegroundColor Green
        Write-Host ""
        Write-Host "========================================" -ForegroundColor Cyan
        Write-Host "Installation Complete!" -ForegroundColor Cyan
        Write-Host "========================================" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "Next steps:" -ForegroundColor Yellow
        Write-Host "1. cd 'e:\PEO SPORTS\sports_scraper'" -ForegroundColor White
        Write-Host "2. python -m venv venv" -ForegroundColor White
        Write-Host "3. venv\Scripts\activate" -ForegroundColor White
        Write-Host "4. pip install -r requirements.txt" -ForegroundColor White
        Write-Host ""
    }
    else {
        Write-Host "✗ Python verification failed" -ForegroundColor Red
        Write-Host "Try opening a new terminal and running: python --version" -ForegroundColor Yellow
        exit 1
    }
}
catch {
    Write-Host "✗ Could not verify Python: $_" -ForegroundColor Red
    Write-Host "Try opening a new terminal and running: python --version" -ForegroundColor Yellow
    exit 1
}

# Cleanup
Remove-Item -Force -ErrorAction SilentlyContinue $installerPath
Write-Host "Cleanup completed." -ForegroundColor Gray
