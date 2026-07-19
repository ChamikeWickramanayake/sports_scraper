# Quick Start Guide

## 5-Minute Setup

### Step 1: Run Setup Script
```powershell
cd "e:\PEO SPORTS\sports_scraper"
.\setup.bat
```
This will:
- Create Python virtual environment
- Install all dependencies
- Verify Python installation

### Step 2: Get Google Credentials
1. Visit [Google Cloud Console](https://console.cloud.google.com/)
2. Create service account → Download JSON key
3. Save as: `config/credentials.json`

### Step 3: Create Google Sheet
1. Go to [Google Sheets](https://sheets.google.com) → New Sheet
2. Copy the **Sheet ID** from URL: `https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit`
3. Share sheet with service account email from credentials.json

### Step 4: Configure Sheet ID
**Windows Command Prompt:**
```cmd
setx GOOGLE_SHEET_ID "your-sheet-id-here"
```

**OR edit `config/config.py`:**
```python
GOOGLE_SHEET_ID = "your-sheet-id-here"
```

### Step 5: Test Run
```powershell
.\venv\Scripts\activate
python main.py
```

Check your Google Sheet — events should appear!

### Step 6: Schedule Daily Run
1. Open Task Scheduler (`Win + R` → `taskschd.msc`)
2. Create Basic Task:
   - Name: "Sports Scraper Daily"
   - Trigger: Daily @ 6:00 AM
   - Action: Run `scheduler.bat`
   - Location: `e:\PEO SPORTS\sports_scraper`

## Testing Individual Scrapers

```powershell
python test_scrapers.py
```

This tests scrapers without needing Google Sheets.

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Python not found" | Install Python 3.8+, add to PATH |
| "Credentials file not found" | Download from Google Cloud Console |
| "GOOGLE_SHEET_ID not configured" | Set environment variable or edit config.py |
| "Sheet not updating" | Verify service account has Edit access |
| "Task fails silently" | Check `logs/scheduler_*.log` |

## File Structure Quick Reference

```
sports_scraper/
├── setup.bat              ← Run this first!
├── main.py                ← Main scraper script
├── test_scrapers.py       ← Test without Google Sheets
├── config/
│   ├── config.py          ← Edit: GOOGLE_SHEET_ID
│   ├── sources.json       ← Edit: enable/disable sources
│   └── credentials.json   ← Add: Google service account key
├── logs/                  ← Check here for errors
├── requirements.txt       ← Python dependencies
└── README.md              ← Full documentation
```

## Next: Manual Testing

```bash
# Activate environment
cd "e:\PEO SPORTS\sports_scraper"
venv\Scripts\activate

# Test scrapers only (no Google Sheets needed)
python test_scrapers.py

# Full run with Google Sheets sync
python main.py
```

## Need Help?

1. Check `logs/scraper.log` for error details
2. Read full documentation in `README.md`
3. Test individual scrapers: `python test_scrapers.py`

---

**All code ready!** Follow the 5 steps above to get started. 🚀
