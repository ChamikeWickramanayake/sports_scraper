# INSTALLATION SUMMARY

## What's Been Created

Your complete sports events scraper project is ready in: `c:\Bassa\sports_scraper\`

**Files Created:**
- Main scraper script (`main.py`)
- Dedicated web scrapers (Cricbuzz, BBC Sport) plus a generic fallback scraper
- Excel export to `output\sports_events_[timestamp].xlsx`
- Configuration files
- Logging system
- Windows Task Scheduler batch file
- All documentation

## Installation Steps

### Step 1: Install Python (CRITICAL)

**If you haven't installed Python yet:**

1. Download Python 3.8+ from https://www.python.org/downloads/
2. Run the installer
3. **IMPORTANT**: Check the box "Add Python to PATH"
4. Click "Install Now"
5. Open a NEW terminal afterwards (PATH changes don't reach already-open ones)

**Alternative: Use the provided installer scripts**
- Double-click: `c:\Bassa\sports_scraper\install_python.bat`
- Or run: `powershell -ExecutionPolicy Bypass -File install_python.ps1`
- Wait for it to complete (2-3 minutes)
- Note: without administrator rights the scripts fall back to a per-user install - that's fine

### Step 2: Run Complete Setup

1. Open Command Prompt or PowerShell
2. Navigate to the project:
   ```
   cd c:\Bassa\sports_scraper
   ```
3. Run the setup:
   ```
   complete_setup.bat
   ```

This will:
- Verify Python is installed
- Create virtual environment
- Install all dependencies (beautifulsoup4, requests, openpyxl)
- Run tests

(`setup.bat` does the same minus the test run.)

### Step 3: Test It

Open Command Prompt in the project folder and run:

```
venv\Scripts\python.exe main.py
```

**Expected:**
- Script runs and scrapes events
- Open `output\sports_events_[timestamp].xlsx` - events appear!
- Check `logs\scraper.log` for details

### Step 4: Schedule Daily Run (Optional)

1. Open Task Scheduler (Win + R -> `taskschd.msc`)
2. Right-click -> "Create Basic Task"
3. Set:
   - Name: "Sports Scraper Daily"
   - Trigger: Daily at 6:00 AM
   - Action: Run program
   - Program: `c:\Bassa\sports_scraper\scheduler.bat`
   - Start in: `c:\Bassa\sports_scraper`
4. Click Finish
5. Right-click task -> Run (to test)

## Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| "Python not found" | Install from python.org, add to PATH, open a NEW terminal |
| Virtual environment fails | Delete `venv` folder, run `complete_setup.bat` again |
| Dependencies won't install | Activate venv first: `venv\Scripts\activate` |
| No events in Excel file | Check `logs\scraper.log`; run `python test_scrapers.py` |
| Excel file won't save | Close `output\sports_events_[timestamp].xlsx` in Excel first |

## Files to Know About

| File | Purpose |
|------|---------|
| `complete_setup.bat` | Run this to set up everything |
| `main.py` | Main scraper - run `python main.py` |
| `test_scrapers.py` | Test the scrapers and Excel export |
| `config/config.py` | Settings (date range, delays, timeouts) |
| `config/sources.json` | List of 28 sports sources to scrape |
| `output/sports_events_[timestamp].xlsx` | The results land here |
| `logs/scraper.log` | Check this for errors/details |
| `README.md` | Full documentation |
| `QUICKSTART.md` | Quick reference |

## Next Actions

1. **Install Python** (if not done)
2. **Run**: `complete_setup.bat`
3. **Test**: `venv\Scripts\python.exe main.py`
4. **Open**: `output\sports_events_[timestamp].xlsx`
5. **Schedule** in Windows Task Scheduler (optional)

---

## Support

- **Full setup guide**: See `SETUP_GUIDE.md`
- **Quick reference**: See `QUICKSTART.md`
- **Complete docs**: See `README.md`
- **Errors?** Check `logs\scraper.log`

**Everything is ready - just follow the steps above!**
