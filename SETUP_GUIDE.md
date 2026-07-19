# Setup Instructions - Sports Events Scraper

## Prerequisites Check

Before running the scraper, ensure you have:
- ✓ Python 3.8+ installed and added to PATH
- ✓ A Google Cloud project with service account credentials
- ✓ A Google Sheet created and shared with service account

## Step-by-Step Setup

### 1. Install Python (if not already installed)

**Windows:**
1. Download from [python.org](https://www.python.org/downloads/)
2. Run the installer
3. **IMPORTANT**: Check "Add Python to PATH" during installation
4. Click "Install Now"

**Verify Installation:**
Open Command Prompt or PowerShell and run:
```cmd
python --version
```

Should show: `Python 3.x.x`

If you see "Python was not found", go to Settings → Apps → Advanced app settings → App execution aliases and disable "python.exe" and "python3.exe" (Windows Store aliases).

### 2. Create Virtual Environment

Open Command Prompt in the project folder:
```cmd
cd "e:\PEO SPORTS\sports_scraper"
python -m venv venv
```

Activate it:
```cmd
venv\Scripts\activate
```

You should see `(venv)` at the start of your prompt.

### 3. Install Dependencies

```cmd
pip install --upgrade pip
pip install -r requirements.txt
```

This will install:
- beautifulsoup4 (web scraping)
- requests (HTTP)
- google-auth-oauthlib (Google auth)
- google-api-python-client (Google Sheets API)
- And others...

### 4. Set Up Google Credentials

#### 4a. Create Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (name: "Sports Scraper")
3. Enable Google Sheets API:
   - Search for "Google Sheets API"
   - Click "Enable"

#### 4b. Create Service Account
1. Go to "Service Accounts" in Google Cloud Console
2. Click "Create Service Account"
3. Fill in:
   - Service account name: "sports-scraper"
   - Service account ID: (auto-filled)
   - Click "Create and Continue"
4. Grant role: **Editor**
5. Click "Continue" → "Done"

#### 4c. Generate JSON Key
1. In Service Accounts, click the new account
2. Go to "Keys" tab
3. Click "Add Key" → "Create new key" → "JSON"
4. A file downloads automatically
5. Move it to: `config/credentials.json`

**⚠️ SECURITY**: Never commit credentials.json to version control!

### 5. Create Google Sheet

1. Go to [Google Sheets](https://sheets.google.com)
2. Create a new blank spreadsheet
3. Name it "Sports Events"
4. Share it with the service account email:
   - Open `config/credentials.json`
   - Find the `"client_email"` field
   - Copy the email address
   - In Google Sheet: Click Share → Paste email → Share

### 6. Configure Sheet ID

#### Option A: Environment Variable (Recommended)

**Command Prompt:**
```cmd
setx GOOGLE_SHEET_ID "your-sheet-id-here"
```

**PowerShell:**
```powershell
[Environment]::SetEnvironmentVariable("GOOGLE_SHEET_ID", "your-sheet-id-here", "User")
```

Then restart your terminal/IDE.

#### Option B: Edit config.py

Open `config/config.py` and change:
```python
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID", "your-sheet-id-here")
```

### 7. Find Your Sheet ID

1. Open your Google Sheet in browser
2. Look at the URL: `https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit`
3. Copy the `{SHEET_ID}` part (long string of characters)
4. Use this in step 6

## Testing

### Test Scrapers Only (No Google Sheets)

```cmd
(venv) cd "e:\PEO SPORTS\sports_scraper"
(venv) python test_scrapers.py
```

This will test scrapers without needing Google Sheets setup. Check output in console.

### Full Test with Google Sheets

Make sure:
1. `config/credentials.json` exists
2. `GOOGLE_SHEET_ID` is set
3. Google Sheet is shared with service account

Then run:
```cmd
(venv) python main.py
```

Check your Google Sheet — events should appear!

## Running Daily

### Option 1: Manual
```cmd
(venv) python main.py
```

### Option 2: Windows Task Scheduler

1. Open Task Scheduler (Press `Win + R`, type `taskschd.msc`)
2. Right-click → Create Basic Task:
   - **Name**: "Sports Scraper Daily"
   - **Trigger**: Daily at 6:00 AM
   - **Action**: Run program
     - Program: `e:\PEO SPORTS\sports_scraper\scheduler.bat`
     - Start in: `e:\PEO SPORTS\sports_scraper`
3. Click Finish
4. Test by right-clicking task → Run

## Troubleshooting

### Error: "Python was not found"
- Disable Microsoft Store Python alias (Settings → Apps → App execution aliases)
- Or use full path: `C:\Users\YOUR_USERNAME\AppData\Local\Programs\Python\Python310\python.exe`

### Error: "Module not found"
- Make sure virtual environment is activated: `(venv)` should show in prompt
- Run: `pip install -r requirements.txt`

### Error: "Credentials file not found"
- Download credentials.json from Google Cloud Console
- Place in: `e:\PEO SPORTS\sports_scraper\config\credentials.json`

### Error: "GOOGLE_SHEET_ID not configured"
- Set environment variable (step 6)
- Or edit `config/config.py`

### Google Sheet not updating
- Verify service account email has Edit access to sheet
- Check `logs/scraper.log` for errors
- Manually run: `python main.py`

## Next Steps

1. Install Python ✓
2. Create virtual environment ✓
3. Install dependencies ✓
4. Set up Google Cloud credentials ✓
5. Create Google Sheet ✓
6. Configure GOOGLE_SHEET_ID ✓
7. Test with `python test_scrapers.py`
8. Run full script with `python main.py`
9. Schedule in Task Scheduler

---

**Questions?** Check `logs/scraper.log` for detailed error messages.
