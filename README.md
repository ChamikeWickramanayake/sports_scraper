# Sports Events Scraper & Google Sheets Sync

Automated Python program to scrape upcoming sports events from multiple trusted sources (ESPN, BBC Sport, Flashscore, Cricinfo, Cricbuzz, etc.) and sync them daily to a Google Sheet with deduplication and date filtering.

## Features

- **Multi-Source Scraping**: 18+ trusted sports news providers
- **Multiple Sports**: Cricket, Football, Basketball, Tennis, Rugby, Baseball, American Football, Hockey, Golf
- **Web Scraping**: BeautifulSoup-based extraction from major sports websites
- **Parallel Execution**: ThreadPoolExecutor for fast concurrent scraping
- **Deduplication**: Smart event matching to prevent duplicates across sources
- **Date Filtering**: Automatically excludes past events, configurable date range
- **Google Sheets Integration**: Automated sync using service account credentials
- **Local Caching**: 24-hour cache to avoid redundant scrapes
- **Error Handling**: Retry logic, fallback scrapers, comprehensive logging
- **Windows Task Scheduler**: Pre-built batch file for daily automation
- **Rate Limiting**: Respectful delays between requests, configurable user-agents

## Project Structure

```
sports_scraper/
├── config/
│   ├── config.py              # Central configuration
│   ├── sources.json           # Source definitions
│   └── credentials.json       # (Create this) Google service account key
├── scrapers/
│   ├── base_scraper.py        # Base class for all scrapers
│   ├── espn_cricinfo_scraper.py
│   ├── bbc_sport_scraper.py
│   ├── flashscore_scraper.py
│   ├── cricbuzz_scraper.py
│   ├── generic_scraper.py     # Fallback for unsupported sources
│   └── scraper_factory.py     # Factory to load and instantiate scrapers
├── utils/
│   ├── logger.py              # Logging configuration
│   ├── auth.py                # Google authentication
│   └── google_sheets.py       # Google Sheets API wrapper
├── logs/                      # Execution logs (auto-created)
├── cache/                     # Local event cache (auto-created)
├── main.py                    # Main orchestrator
├── scheduler.bat              # Windows Task Scheduler wrapper
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Setup Instructions

### 1. Install Python & Dependencies

```bash
# Navigate to project directory
cd "e:\PEO SPORTS\sports_scraper"

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Google Cloud Setup

#### Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (e.g., "Sports Events Scraper")
3. Enable the **Google Sheets API**:
   - Search for "Google Sheets API"
   - Click "Enable"

#### Create a Service Account

1. In Google Cloud Console, go to **Service Accounts**
2. Click **Create Service Account**
3. Fill in details (e.g., name: "sports-scraper")
4. Click **Create and Continue**
5. Grant role: **Editor** (or limited permissions if preferred)
6. Click **Continue** → **Done**

#### Generate Credentials

1. In Service Accounts, click the newly created account
2. Go to **Keys** tab
3. Click **Add Key** → **Create New Key** → **JSON**
4. The credentials file downloads automatically
5. Move this file to: `config/credentials.json`

**⚠️ Important**: Keep `credentials.json` secure. Add it to `.gitignore` if using version control.

### 3. Create Google Sheet

1. Create a new Google Sheet at [Google Sheets](https://sheets.google.com)
2. Name it "Sports Events" (or your preference)
3. Share it with the service account email from `credentials.json`:
   - Open `credentials.json` and copy the `client_email` value
   - Go to your Google Sheet → **Share** → Paste email → **Share**

4. Get the **Sheet ID** (from the URL):
   - URL format: `https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit`
   - Copy the `{SHEET_ID}` value

### 4. Configure the Application

**Option A: Environment Variable** (Recommended)

```bash
# Set environment variable (Windows Command Prompt)
setx GOOGLE_SHEET_ID "your-sheet-id-here"

# OR PowerShell
[Environment]::SetEnvironmentVariable("GOOGLE_SHEET_ID", "your-sheet-id-here", "User")

# Restart terminal/IDE for changes to take effect
```

**Option B: Direct Configuration**

Edit `config/config.py`:

```python
GOOGLE_SHEET_ID = "your-sheet-id-here"  # Replace with actual ID
```

### 5. Test the Scraper

```bash
# Activate virtual environment
venv\Scripts\activate

# Run the scraper
python main.py
```

**Expected Output:**
- Check `logs/scraper.log` for execution details
- Events should appear in your Google Sheet

## Usage

### Manual Execution

```bash
cd "e:\PEO SPORTS\sports_scraper"
venv\Scripts\activate
python main.py
```

### Schedule with Windows Task Scheduler

#### Create the Task

1. Open **Task Scheduler** (Press `Win + R`, type `taskschd.msc`, press Enter)
2. Click **Create Basic Task** (right panel)
3. **Name**: "Sports Scraper Daily"
4. **Description**: "Daily fetch and sync sports events"
5. Click **Next**

#### Set Trigger

1. Select **Daily**
2. Set **Start date** and **time** (e.g., 6:00 AM)
3. Set **Recur every**: 1 day
4. Click **Next**

#### Set Action

1. Select **Start a program**
2. **Program/script**: `e:\PEO SPORTS\sports_scraper\scheduler.bat`
3. **Start in**: `e:\PEO SPORTS\sports_scraper`
4. Click **Next** → **Finish**

#### Test the Task

1. In Task Scheduler, find your task
2. Right-click → **Run**
3. Wait a few seconds
4. Check `logs/` folder for `scheduler_*.log`
5. Verify events in Google Sheet

## Configuration

### Edit Data Sources

Modify `config/sources.json` to enable/disable sources:

```json
{
  "enabled": false,  // Set to false to disable scraping from this source
  "scraper_type": "generic"  // Use "generic" for unsupported sites
}
```

### Adjust Date Range

Edit `config/config.py`:

```python
MIN_EVENT_DAYS_AHEAD = 0        # Include events from today (0) or future only (1)
MAX_EVENT_DAYS_AHEAD = 365      # Include events up to X days ahead
```

### Change Cache Duration

```python
CACHE_EXPIRY_HOURS = 24  # Keep cached data for 24 hours
```

### Adjust Concurrency

Edit `main.py` in the `run()` method:

```python
orchestrator.run(max_workers=10)  # Default is 5, increase for faster scraping
```

## Output

### Google Sheet Columns

| Column | Description |
|--------|-------------|
| Sport | Sport type (Cricket, Football, etc.) |
| Event | Match/Event name |
| Broadcasting Partner | Channel or broadcaster |
| Event Date | Date and time of event |
| Location | Event venue/city |
| Teams | Participating teams |
| Source | Which website the event came from |
| Last Updated | When the row was added to sheet |

### Logs

Logs are saved to:
- Daily logs: `logs/scraper.log`
- Task Scheduler logs: `logs/scheduler_YYYY-MM-DD_HHMM.log`

## Troubleshooting

### Issue: "Credentials file not found"

**Solution**: 
- Download `credentials.json` from Google Cloud Console
- Place in `config/credentials.json`

### Issue: "GOOGLE_SHEET_ID not configured"

**Solution**:
- Set environment variable: `GOOGLE_SHEET_ID`
- Or update `config/config.py` directly

### Issue: "No rows appearing in Google Sheet"

**Solutions**:
1. Verify service account email has **Edit** access to the sheet
2. Check `logs/scraper.log` for errors
3. Verify `credentials.json` is valid
4. Ensure `GOOGLE_SHEET_ID` is correct (no extra spaces)

### Issue: "Task Scheduler task fails silently"

**Solution**:
1. Check `logs/scheduler_*.log` for error details
2. Run `scheduler.bat` manually to see errors
3. Verify virtual environment path in `scheduler.bat` is correct

### Issue: "Website returns 403 or 429 errors"

**Solution**:
- Increase delay between requests in `config/config.py`:
  ```python
  REQUEST_DELAY = 5  # Increase from 2 to 5 seconds
  ```
- Some sites may block automated requests. Consider using their APIs instead.

## Scaling & Maintenance

### Add New Sports Websites

1. **If site has available API**: Use it directly (faster, more reliable)
2. **For web scraping**:
   - Add entry to `config/sources.json`
   - Create custom scraper in `scrapers/` (inherit from `BaseScraper`)
   - Implement `scrape()` method
   - Add to `SCRAPER_CLASSES` dict in `scraper_factory.py`

### Performance Optimization

- Increase `max_workers` in `main.py` for faster parallel scraping
- Use caching to skip redundant scrapes within 24 hours
- Disable sources with rate-limiting issues

### Website Structure Changes

Cricket websites frequently update their HTML structure. If scraping stops working:

1. Check `logs/scraper.log` for parse errors
2. Update CSS selectors in the relevant scraper
3. Test with `python main.py`

## Dependencies

- **beautifulsoup4**: HTML parsing
- **requests**: HTTP requests with retries
- **selenium**: (Optional) For JavaScript-heavy sites
- **google-auth-oauthlib**: Google authentication
- **google-api-python-client**: Google Sheets API
- **openpyxl**: Excel file reading (future feature)

## Future Enhancements

- [ ] Email/SMS notifications for major events
- [ ] Advanced filtering by team, league, broadcaster
- [ ] Historical data analysis
- [ ] Event ticket link extraction
- [ ] Real-time score updates
- [ ] Mobile app integration

## Support

For issues or questions:
1. Check `logs/scraper.log` for error details
2. Verify all setup steps were completed
3. Test individual scrapers with `python -c "from scrapers.espn_cricinfo_scraper import ESPNCricinfoScraper; s = ESPNCricinfoScraper(); print(s.scrape())"`

## License

Private use. Respect website terms of service when scraping.
