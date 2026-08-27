# Setup Instructions - Sports Events Scraper

## Prerequisites Check

Before running the scraper, ensure you have:
- Python 3.8+ installed and added to PATH

That's all - the scraper writes to a local Excel file, so there are no accounts, API keys, or credentials to set up.

## Step-by-Step Setup

### 1. Install Python (if not already installed)

**Windows:**
1. Download from [python.org](https://www.python.org/downloads/)
2. Run the installer
3. **IMPORTANT**: Check "Add Python to PATH" during installation
4. Click "Install Now"

Or use the provided installer script:
```cmd
powershell -ExecutionPolicy Bypass -File install_python.ps1
```
(If not run as administrator, it falls back to a per-user install. Open a NEW terminal afterwards so the PATH change takes effect.)

**Verify Installation:**
Open a NEW Command Prompt or PowerShell and run:
```cmd
python --version
```

Should show: `Python 3.x.x`

If you see "Python was not found", go to Settings -> Apps -> Advanced app settings -> App execution aliases and disable "python.exe" and "python3.exe" (Windows Store aliases). See `PYTHON_INSTALLATION_HELP.md` for more troubleshooting.

### 2. Create Virtual Environment

Open Command Prompt in the project folder:
```cmd
cd c:\Bassa\sports_scraper
python -m venv venv
```

Activate it:
```cmd
venv\Scripts\activate
```

You should see `(venv)` at the start of your prompt.

(Shortcut: `setup.bat` performs steps 2 and 3 for you; `complete_setup.bat` also runs the test suite afterwards.)

### 3. Install Dependencies

```cmd
pip install --upgrade pip
pip install -r requirements.txt
```

This will install:
- beautifulsoup4 (web scraping)
- requests (HTTP)
- openpyxl (Excel export)

That's the complete dependency list.

## Testing

```cmd
(venv) cd c:\Bassa\sports_scraper
(venv) python test_scrapers.py
```

This parses offline HTML fixtures in `tests/fixtures/`, live-tests the first 3 enabled scrapers, and tests the Excel export. Exit code 0 means everything passed. Check output in console and `logs/scraper.log`.

## Full Run

```cmd
(venv) python main.py
```

Open `output\sports_events_[timestamp].xlsx` - events should appear! Each run creates its own new timestamped file.

## Running Daily

### Option 1: Manual
```cmd
(venv) python main.py
```

### Option 2: Windows Task Scheduler

1. Open Task Scheduler (Press `Win + R`, type `taskschd.msc`)
2. Right-click -> Create Basic Task:
   - **Name**: "Sports Scraper Daily"
   - **Trigger**: Daily at 6:00 AM
   - **Action**: Run program
     - Program: `c:\Bassa\sports_scraper\scheduler.bat`
     - Start in: `c:\Bassa\sports_scraper`
3. Click Finish
4. Test by right-clicking task -> Run

`scheduler.bat` uses `venv\Scripts\python.exe` when the virtual environment exists and falls back to the system `python` otherwise. Each run writes its own log to `logs\scheduler_<timestamp>.log` - check there if a scheduled run fails.

## Troubleshooting

### Error: "Python was not found"
- Disable Microsoft Store Python alias (Settings -> Apps -> App execution aliases)
- Or use full path: `C:\Users\YOUR_USERNAME\AppData\Local\Programs\Python\Python311\python.exe`

### Error: "Module not found"
- Make sure virtual environment is activated: `(venv)` should show in prompt
- Run: `pip install -r requirements.txt`

### Excel file not updating
- Close `output\sports_events_[timestamp].xlsx` in Excel - an open workbook is locked for writing
- Check `logs/scraper.log` for errors
- Manually run: `python main.py`

### A source returns no events
- Only `cricbuzz` and `bbc_sport` have dedicated scrapers with reliable dates; the other enabled sources use a generic heuristic scraper (low confidence, dates often "TBD")
- Four sources are intentionally disabled in `config/sources.json` (see their `disabled_reason`): `espn` and `espn_cricinfo` (Akamai bot protection), `flashscore` and `livescore` (client-rendered, need a browser)

## Next Steps

1. Install Python
2. Create virtual environment (or run `setup.bat`)
3. Install dependencies
4. Test with `python test_scrapers.py`
5. Run full script with `python main.py`
6. Open `output\sports_events_[timestamp].xlsx`
7. Schedule in Task Scheduler

---

**Questions?** Check `logs/scraper.log` for detailed error messages.
