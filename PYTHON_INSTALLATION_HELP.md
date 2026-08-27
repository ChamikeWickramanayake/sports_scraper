# Python Installation Troubleshooting Guide

## Issue: Python Installer Keeps Failing

The official Python installer has encountered issues on this system. Follow one of these solutions:

## Solution 1: Manual Installation (Recommended if GUI fails)

1. **Download Python manually:**
   - Go to: https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe
   - Save to your Desktop

2. **Install with correct options:**
   - Double-click the downloaded .exe file
   - **CRITICAL**: Check BOTH of these boxes:
     - [x] "Install launcher for all users"
     - [x] "Add Python 3.11 to PATH"
   - Click "Customize installation"
   - Check all optional features (pip, tcltk, dev tools)
   - Click "Next"
   - Check "Install for all users" and "Precompile standard library"
   - Click "Install"

3. **Verify Installation:**
   - Close all terminals/PowerShell windows completely - PATH changes only reach NEW terminals
   - Open a NEW Command Prompt (not PowerShell)
   - Type: `python --version`
   - Should show: `Python 3.11.9`

## Solution 2: Use the Provided Install Scripts

From the project folder (`c:\Bassa\sports_scraper`):

```powershell
powershell -ExecutionPolicy Bypass -File install_python.ps1
```

Or double-click `install_python.bat` (silent) or `install_python_gui.bat` (shows the installer window).

Notes:
- If not run as administrator, the scripts fall back to a **per-user install** (under `%LOCALAPPDATA%\Programs\Python`) - this works fine for this project.
- PATH changes require a **NEW terminal**: close your terminal and open a fresh one before running `python --version`.

## Solution 3: Alternative Installation (If Python.org fails)

**Using Windows Package Manager (winget):**
```powershell
winget install Python.Python.3.11
```

Then verify (in a NEW terminal):
```
python --version
```

## Solution 4: Using Portable Python (No installation needed)

If standard installation fails completely:

1. Download the "Windows embeddable package" from: https://www.python.org/downloads/windows/
2. Extract to: `C:\Python311-portable`
3. Then use the full path when running Python:
   ```
   C:\Python311-portable\python.exe -m pip install -r requirements.txt
   ```

## Solution 5: Use Microsoft Store Python

```powershell
# Open Settings > Apps > Apps & features > Get more apps
# Search for "Python 3.11"
# Install from Microsoft Store
```

## After Python is Installed

1. **Verify Python** (in a NEW terminal):
   ```
   python --version
   pip --version
   ```

2. **Navigate to project:**
   ```
   cd c:\Bassa\sports_scraper
   ```

3. **Create virtual environment:**
   ```
   python -m venv venv
   venv\Scripts\activate
   ```

4. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

   (Steps 3-4 can also be done for you by running `setup.bat`.)

5. **Run the scraper:**
   ```
   python main.py
   ```

## Common Issues After Installation

### Issue: "python not found" even after installation

**Solution:**
- Close all terminals completely - an already-open terminal keeps the old PATH
- Open a NEW Command Prompt (cmd.exe, not PowerShell)
- Try again

### Issue: PATH not updated

**Solution - Add Python to PATH manually:**

1. Find your Python installation:
   - Per-user install: `C:\Users\YourUsername\AppData\Local\Programs\Python\Python311`
   - All-users install: `C:\Program Files\Python311`

2. Add to PATH:
   ```powershell
   $pythonPath = "C:\Users\$env:USERNAME\AppData\Local\Programs\Python\Python311"
   [Environment]::SetEnvironmentVariable(
       "Path",
       "$env:Path;$pythonPath;$pythonPath\Scripts",
       "User"
   )
   ```

3. Close and reopen terminal

### Issue: "pip" not found

**Solution:**
```
python -m pip install --upgrade pip
```

## Quick Test Script

Copy this into a file called `test_python.bat` and run it:

```batch
@echo off
echo Testing Python installation...
python --version
if %ERRORLEVEL% equ 0 (
    echo [OK] Python is working!
    python -c "import sys; print(f'Python location: {sys.executable}')"
    pip --version
) else (
    echo [X] Python not found
    echo Try: python -c "import sys; print(sys.executable)"
)
pause
```

## Next Steps After Python Works

Once Python is installed:

1. Run: `cd c:\Bassa\sports_scraper`
2. Run: `setup.bat` (creates the venv and installs dependencies)
3. Run: `python main.py`
4. Open the results: `output\sports_events_[timestamp].xlsx`

## Need Help?

Check our documentation:
- `README.md` - Full reference
- `QUICKSTART.md` - Quick start guide
- `SETUP_GUIDE.md` - Detailed setup steps
- `START_HERE.md` - Get started overview

## Still Having Issues?

Try this diagnostic script:

```
python -c "import sys; print('Python:', sys.version); print('Executable:', sys.executable); print('Path:', sys.path)"
```

This will show:
- Your Python version
- Where Python is installed
- All installed modules paths
