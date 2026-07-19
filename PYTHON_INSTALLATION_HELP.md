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
     - ☑ "Install launcher for all users"
     - ☑ "Add Python 3.11 to PATH"
   - Click "Customize installation"
   - Check all optional features (pip, tcltk, dev tools)
   - Click "Next"
   - Check "Install for all users" and "Precompile standard library"
   - Click "Install"

3. **Verify Installation:**
   - Close all terminals/PowerShell windows completely
   - Open a NEW Command Prompt (not PowerShell)
   - Type: `python --version`
   - Should show: `Python 3.11.9`

## Solution 2: Alternative Installation (If Python.org fails)

**Using Windows Package Manager (winget):**
```powershell
winget install Python.Python.3.11
```

Then verify:
```
python --version
```

## Solution 3: Using Portable Python (No installation needed)

If standard installation fails completely:

1. Download portable Python from: https://github.com/pypa/get-pip/blob/main/public/index.html
2. Extract to: `C:\Python311-portable`
3. Then use the full path when running Python:
   ```
   C:\Python311-portable\python.exe -m pip install -r requirements.txt
   ```

## Solution 4: Use Microsoft Store Python

```powershell
# Open Settings > Apps > Apps & features > Get more apps
# Search for "Python 3.11"
# Install from Microsoft Store
```

## After Python is Installed

1. **Verify Python:**
   ```
   python --version
   pip --version
   ```

2. **Navigate to project:**
   ```
   cd "e:\PEO SPORTS\sports_scraper"
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

5. **Run the scraper:**
   ```
   python main.py
   ```

## Common Issues After Installation

### Issue: "python not found" even after installation

**Solution:**
- Close all terminals completely
- Open a NEW Command Prompt (cmd.exe, not PowerShell)
- Try again

### Issue: PATH not updated

**Solution - Add Python to PATH manually:**

1. Find your Python installation:
   - Usually: `C:\Users\YourUsername\AppData\Local\Programs\Python\Python311`
   - Or: `C:\Program Files\Python311`

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
    echo ✓ Python is working!
    python -c "import sys; print(f'Python location: {sys.executable}')"
    pip --version
) else (
    echo ✗ Python not found
    echo Try: python -c "import sys; print(sys.executable)"
)
pause
```

## Next Steps After Python Works

Once Python is installed:

1. Run: `cd "e:\PEO SPORTS\sports_scraper"`
2. Run: `python main.py`
3. Then set up Google Sheets credentials

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
