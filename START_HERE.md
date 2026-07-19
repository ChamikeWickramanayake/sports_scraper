# INSTALLATION SUMMARY

## What's Been Created ✅

Your complete sports events scraper project is ready in: `e:\PEO SPORTS\sports_scraper\`

**Files Created:**
- ✓ Main scraper script (`main.py`)
- ✓ 5 specialized web scrapers (ESPN Cricinfo, BBC Sport, Flashscore, Cricbuzz, etc.)
- ✓ Google Sheets API integration
- ✓ Configuration files
- ✓ Logging system
- ✓ Windows Task Scheduler batch file
- ✓ All documentation

## Installation Steps

### Step 1: Install Python (CRITICAL)

**If you haven't installed Python yet:**

1. Download Python 3.8+ from https://www.python.org/downloads/
2. Run the installer
3. **IMPORTANT**: Check the box "Add Python to PATH"
4. Click "Install Now"
5. Restart your computer

**Alternative: Use the provided installer script**
- Double-click: `e:\PEO SPORTS\sports_scraper\install_python.bat`
- Wait for it to complete (2-3 minutes)

### Step 2: Run Complete Setup

1. Open Command Prompt or PowerShell
2. Navigate to the project:
   ```
   cd "e:\PEO SPORTS\sports_scraper"
   ```
3. Run the setup:
   ```
   complete_setup.bat
   ```

This will:
- ✓ Verify Python is installed
- ✓ Create virtual environment
- ✓ Install all dependencies
- ✓ Run tests

### Step 3: Google Sheets Setup (5 minutes)

#### 3a. Get Google Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable Google Sheets API (search for it)
4. Create Service Account:
   - Go to "Service Accounts"
   - Create new service account
   - Click the account → "Keys" tab
   - "Create new key" → JSON
5. Download file and save to:
   ```
   e:\PEO SPORTS\sports_scraper\config\credentials.json
   ```

#### 3b. Create Google Sheet

1. Go to https://sheets.google.com
2. Create new blank spreadsheet
3. Name it "Sports Events"
4. Share it with the service account email from credentials.json
5. Copy the Sheet ID from the URL:
   - URL: `https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit`
   - Copy the long string: `{SHEET_ID}`

#### 3c. Set Sheet ID

**Option A: Command Prompt (easiest)**
```
setx GOOGLE_SHEET_ID "your-sheet-id-here"
```
Then close and reopen Command Prompt.

**Option B: Edit config file**
- Open: `e:\PEO SPORTS\sports_scraper\config\config.py`
- Find: `GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID", "")`
- Change to: `GOOGLE_SHEET_ID = "your-sheet-id-here"`

### Step 4: Test It

Open Command Prompt in the project folder and run:

```
python main.py
```

**Expected:**
- Script runs and scrapes events
- Check your Google Sheet — events appear!
- Check logs/scraper.log for details

### Step 5: Schedule Daily Run (Optional)

1. Open Task Scheduler (Win + R → `taskschd.msc`)
2. Right-click → "Create Basic Task"
3. Set:
   - Name: "Sports Scraper Daily"
   - Trigger: Daily at 6:00 AM
   - Action: Run program
   - Program: `e:\PEO SPORTS\sports_scraper\scheduler.bat`
   - Start in: `e:\PEO SPORTS\sports_scraper`
4. Click Finish
5. Right-click task → Run (to test)

## Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| "Python not found" | Install from python.org, add to PATH, restart computer |
| Virtual environment fails | Delete `venv` folder, run `complete_setup.bat` again |
| Dependencies won't install | Activate venv first: `venv\Scripts\activate` |
| No events in Google Sheet | Check credentials.json exists, service account has Edit access |
| "GOOGLE_SHEET_ID not configured" | Set environment variable or edit config.py |

## Files to Know About

| File | Purpose |
|------|---------|
| `complete_setup.bat` | Run this to set up everything |
| `main.py` | Main scraper — run `python main.py` |
| `test_scrapers.py` | Test scrapers without Google Sheets |
| `config/config.py` | Settings (edit GOOGLE_SHEET_ID here if needed) |
| `config/sources.json` | List of 18+ sports sources to scrape |
| `config/credentials.json` | Add your Google service account key here |
| `logs/scraper.log` | Check this for errors/details |
| `README.md` | Full documentation |
| `QUICKSTART.md` | Quick reference |

## Next Actions

1. **Install Python** (if not done)
2. **Run**: `complete_setup.bat`
3. **Get Google credentials** and save to `config/credentials.json`
4. **Create Google Sheet** and share with service account
5. **Set GOOGLE_SHEET_ID** environment variable
6. **Test**: `python main.py`
7. **Schedule** in Windows Task Scheduler (optional)

---

## Support

- **Full setup guide**: See `SETUP_GUIDE.md`
- **Quick reference**: See `QUICKSTART.md`
- **Complete docs**: See `README.md`
- **Errors?** Check `logs/scraper.log`

**Everything is ready — just follow the 5 steps above!** 🚀
