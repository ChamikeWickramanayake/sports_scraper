# Quick Start Guide

## 5-Minute Setup

### Step 1: Run Setup Script
```powershell
cd c:\Bassa\sports_scraper
.\setup.bat
```
This will:
- Verify Python installation
- Create Python virtual environment
- Install all dependencies (beautifulsoup4, requests, openpyxl)

(Alternatively run `.\complete_setup.bat` - same steps, plus it runs the test suite at the end.)

### Step 2: Run the Scraper
```powershell
venv\Scripts\python.exe main.py
```

### Step 3: Open the Results

Open `output\sports_events.xlsx` - events should appear!

Re-running appends new events and skips duplicates automatically.

### Step 4: Schedule Daily Run (Optional)
1. Open Task Scheduler (`Win + R` -> `taskschd.msc`)
2. Create Basic Task:
   - Name: "Sports Scraper Daily"
   - Trigger: Daily @ 6:00 AM
   - Action: Run `c:\Bassa\sports_scraper\scheduler.bat`
   - Start in: `c:\Bassa\sports_scraper`

Each scheduled run writes its own log to `logs\scheduler_<timestamp>.log`.

## Testing the Scrapers

```powershell
venv\Scripts\python.exe test_scrapers.py
```

This parses offline HTML fixtures in `tests/fixtures/`, live-tests the first 3 enabled scrapers, and tests the Excel export. Exit code 0 = pass.

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Python not found" | Install Python 3.8+, add to PATH (see `PYTHON_INSTALLATION_HELP.md`) |
| "Module not found" | Run `setup.bat` again, or `venv\Scripts\python.exe -m pip install -r requirements.txt` |
| Excel file won't save | Close `output\sports_events.xlsx` in Excel before running |
| Few/no events from a source | Only `cricbuzz` and `bbc_sport` have dedicated scrapers; the rest are heuristic |
| "Task fails silently" | Check `logs\scheduler_*.log` |

## File Structure Quick Reference

```
sports_scraper/
+-- setup.bat              <- Run this first!
+-- complete_setup.bat     <- Same, plus runs the tests
+-- main.py                <- Main scraper script
+-- test_scrapers.py       <- Test the scrapers and Excel export
+-- config/
|   +-- config.py          <- Settings (date range, delays, timeouts)
|   +-- sources.json       <- Edit: enable/disable sources
+-- output/                <- sports_events.xlsx lands here
+-- logs/                  <- Check here for errors
+-- requirements.txt       <- Python dependencies
+-- README.md              <- Full documentation
```

## Next: Manual Testing

```bash
# Activate environment
cd c:\Bassa\sports_scraper
venv\Scripts\activate

# Test scrapers and Excel export
python test_scrapers.py

# Full run
python main.py
```

## Need Help?

1. Check `logs/scraper.log` for error details
2. Read full documentation in `README.md`
3. Test individual scrapers: `python test_scrapers.py`

---

**All code ready!** Follow the steps above to get started.
