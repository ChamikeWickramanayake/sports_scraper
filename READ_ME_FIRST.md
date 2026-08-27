# PYTHON INSTALLATION MANUAL REQUIRED

## Current Status

Python automated installation has encountered persistent issues on this system. The official Python installer is running but not completing successfully. **You need to install Python manually.**

## What's Ready

- Complete sports scraper project created
- Dedicated web scrapers (Cricbuzz, BBC Sport) plus a generic fallback scraper
- Excel export ready (`output\sports_events.xlsx`)
- All configuration files created
- Windows Task Scheduler support ready
- Complete documentation written

Python installation **still needed**

## What You Need to Do NOW

### Step 1: Install Python Manually (5 minutes)

**BEST METHOD - Download & Run Installer:**

1. Download: https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe

2. **RUN THE INSTALLER** (double-click the .exe file)

3. **IMPORTANT** - Check these boxes:
   - [x] "Add Python 3.11 to PATH" (REQUIRED)
   - [x] "Install launcher for all users"

4. Click "Install Now"

5. Wait for completion

**Alternative - provided script:**
```
powershell -ExecutionPolicy Bypass -File install_python.ps1
```
(Without administrator rights it falls back to a per-user install - that's fine.)

---

### Step 2: Verify Python Works

Open a **NEW** Command Prompt (PATH changes don't reach already-open terminals) and run:
```
python --version
```

Should show: `Python 3.11.9`

---

### Step 3: Run Project Setup

```
cd c:\Bassa\sports_scraper
complete_setup.bat
```

This will:
- Create virtual environment
- Install all dependencies (beautifulsoup4, requests, openpyxl)
- Run tests

---

### Step 4: Run It!

```
python main.py
```

Open `output\sports_events.xlsx` - events will appear!

---

## If Python Installation Fails

See: [PYTHON_INSTALLATION_HELP.md](PYTHON_INSTALLATION_HELP.md)

Options include:
- Windows Package Manager: `winget install Python.Python.3.11`
- Microsoft Store Python
- Portable Python alternative

---

## File Organization

All files are in: `c:\Bassa\sports_scraper\`

**Documentation:**
- `START_HERE.md` - Overview
- `QUICKSTART.md` - Quick reference
- `SETUP_GUIDE.md` - Detailed setup
- `PYTHON_INSTALLATION_HELP.md` - Python troubleshooting
- `README.md` - Full documentation

**Setup Scripts:**
- `complete_setup.bat` - Main setup (run after Python is installed)
- `install_python.ps1` - Python installer (run with: `powershell -ExecutionPolicy Bypass -File install_python.ps1`)
- `install_python_gui.bat` - Manual Python installer
- `install_python_direct.bat` - Alternative installer
- `scheduler.bat` - Task scheduler wrapper

**Core Application:**
- `main.py` - Main scraper (run with: `python main.py`)
- `test_scrapers.py` - Test the scrapers and Excel export
- `scrapers/` - Individual scrapers
- `config/` - Settings and configuration
- `utils/` - Excel export, logging

---

## Quick Summary

1. **Install Python** (download & run)
2. **Run**: `complete_setup.bat`
3. **Run**: `python main.py`
4. **Done!** Events appear in `output\sports_events.xlsx`

---

## Support

**Python won't install?**
-> Read: [PYTHON_INSTALLATION_HELP.md](PYTHON_INSTALLATION_HELP.md)

**Setup questions?**
-> Read: [SETUP_GUIDE.md](SETUP_GUIDE.md)

**Usage questions?**
-> Read: [README.md](README.md)

---

**Next Action**: Download and run Python 3.11.9 installer manually from https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe

Then run: `complete_setup.bat`
