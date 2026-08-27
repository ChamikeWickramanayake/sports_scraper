# Sports Events Scraper

Automated Python program to scrape upcoming sports events from multiple trusted sources (Cricbuzz, BBC Sport, ICC, NBA, etc.) and save them to a local Excel file with deduplication and date filtering.

## Features

- **Multi-Source Scraping**: 28 sports news providers defined in `config/sources.json`
- **Multiple Sports**: Cricket, Football, Basketball, Tennis, Rugby, Baseball, American Football, Hockey, Golf
- **Web Scraping**: BeautifulSoup-based extraction from major sports websites
- **Parallel Execution**: ThreadPoolExecutor for fast concurrent scraping
- **Deduplication**: Smart event matching to prevent duplicates across sources within a run
- **Date Filtering**: Automatically excludes past events, configurable date range
- **Excel Export**: Each run writes its own timestamped file `output/sports_events_[timestamp].xlsx` (no cloud services, no credentials)
- **Local Caching**: 24-hour cache to avoid redundant scrapes
- **Error Handling**: Retry logic, fallback scrapers, comprehensive logging
- **Windows Task Scheduler**: Pre-built batch file for daily automation
- **Rate Limiting**: Respectful delays between requests, configurable user-agents

## Project Structure

```
sports_scraper/
+-- config/
|   +-- config.py              # Central configuration
|   +-- sources.json           # Source definitions (28 sources)
+-- scrapers/
|   +-- base_scraper.py        # Base class for all scrapers
|   +-- cricbuzz_scraper.py    # Dedicated scraper (real dates/venues)
|   +-- bbc_sport_scraper.py   # Dedicated scraper (real dates)
|   +-- espn_cricinfo_scraper.py  # Disabled stub (bot protection)
|   +-- flashscore_scraper.py     # Disabled stub (needs a browser)
|   +-- generic_scraper.py     # Heuristic fallback for other sources
|   +-- scraper_factory.py     # Factory to load and instantiate scrapers
+-- utils/
|   +-- logger.py              # Logging configuration
|   +-- excel_export.py        # Excel file writer (openpyxl)
+-- tests/
|   +-- fixtures/              # Saved HTML pages for offline parser tests
+-- output/                    # Excel output (auto-created)
+-- logs/                      # Execution logs (auto-created)
+-- cache/                     # Local event cache (auto-created)
+-- main.py                    # Main orchestrator
+-- test_scrapers.py           # Test script
+-- setup.bat                  # Quick setup (venv + dependencies)
+-- complete_setup.bat         # Setup + runs the test suite
+-- run.bat                    # Double-click launcher for manual runs
+-- scheduler.bat              # Windows Task Scheduler wrapper
+-- requirements.txt           # Python dependencies
+-- README.md                  # This file
```

## Setup Instructions

### 1. Install Python & Dependencies

**Option A: Run the setup script** (recommended)

```bash
cd c:\Bassa\sports_scraper
setup.bat
```

(`complete_setup.bat` does the same and also runs the test suite at the end.)

**Option B: Manual setup**

```bash
# Navigate to project directory
cd c:\Bassa\sports_scraper

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

If Python itself is not installed yet, see `PYTHON_INSTALLATION_HELP.md`, or run the provided installer script:

```bash
powershell -ExecutionPolicy Bypass -File install_python.ps1
```

### 2. Test the Scraper

```bash
# Activate virtual environment
venv\Scripts\activate

# Run the test suite (exit code 0 = pass)
python test_scrapers.py
```

The test script parses offline HTML fixtures in `tests/fixtures/`, live-tests the first 3 enabled scrapers, and tests the Excel export.

### 3. Run It

```bash
python main.py
```

**Expected Output:**
- Check `logs/scraper.log` for execution details
- Events appear in `output/sports_events_[timestamp].xlsx`

That's it - there is nothing else to configure. No accounts, no API keys, no credentials.

## Usage

### Manual Execution

**Easiest**: double-click `run.bat` - it first asks:

```
Enter a link to scrape (or press Enter to scrape all configured sources):
```

Press Enter to run the normal full scrape, or paste a specific link to scrape only that page (it then asks for an optional sport name - press Enter to auto-detect). Output is shown live in the console, and the window waits for a keypress before closing. It uses the virtual environment automatically (or system Python if the venv is missing).

From a terminal:

```bash
cd c:\Bassa\sports_scraper
venv\Scripts\activate

# Scrape all configured sources
python main.py

# Scrape one specific link only
python main.py --url https://www.example.com/fixtures

# Same, with an explicit sport label (auto-detected if omitted)
python main.py --url https://www.example.com/fixtures --sport Cricket
```

A manual link is scraped with the generic heuristic scraper, so results are low-confidence (dates may be "TBD") and land in that run's own Excel file. Each run writes its own timestamped Excel file, so manual runs never interfere with scheduled ones.

### Schedule with Windows Task Scheduler

#### Quick way (one command)

```cmd
schtasks /create /tn "Sports Events Scraper" /tr "\"c:\Bassa\sports_scraper\scheduler.bat\"" /sc daily /st 08:00
```

This runs the scraper daily at 8:00 AM. Useful follow-ups:

```cmd
schtasks /run /tn "Sports Events Scraper"      :: trigger a run right now
schtasks /query /tn "Sports Events Scraper"    :: check status / next run time
schtasks /delete /tn "Sports Events Scraper"   :: remove the task
```

Note: created this way, the task only runs while the user is logged on. To run it regardless, add `/ru <username> /rp <password>`, or tick "Run whether user is logged on or not" in the Task Scheduler GUI.

#### GUI way

1. Open **Task Scheduler** (Press `Win + R`, type `taskschd.msc`, press Enter)
2. Click **Create Basic Task** (right panel)
3. **Name**: "Sports Scraper Daily"
4. **Description**: "Daily fetch of sports events to Excel"
5. Click **Next**

#### Set Trigger

1. Select **Daily**
2. Set **Start date** and **time** (e.g., 6:00 AM)
3. Set **Recur every**: 1 day
4. Click **Next**

#### Set Action

1. Select **Start a program**
2. **Program/script**: `c:\Bassa\sports_scraper\scheduler.bat`
3. **Start in**: `c:\Bassa\sports_scraper`
4. Click **Next** -> **Finish**

`scheduler.bat` uses `venv\Scripts\python.exe` if the virtual environment exists and falls back to the system `python` otherwise. Each run writes its own log to `logs/scheduler_<timestamp>.log`.

#### Test the Task

1. In Task Scheduler, find your task
2. Right-click -> **Run**
3. Wait a few seconds
4. Check `logs/` folder for `scheduler_*.log`
5. Verify events in `output/sports_events_[timestamp].xlsx`

## Configuration

### Edit Data Sources

Modify `config/sources.json` to enable/disable sources:

```json
{
  "enabled": false,  // Set to false to disable scraping from this source
  "scraper_type": "generic"  // Use "generic" for sites without a dedicated scraper
}
```

Sources in `sources.json` fall into three groups:

- **Dedicated scrapers** - `cricbuzz` (parses the Cricbuzz upcoming-series schedule; real dates and venues) and `bbc_sport` (parses BBC scores-fixtures pages for Football and Cricket; real dates).
- **Disabled sources** (kept in the file with a `disabled_reason`): `espn_cricinfo`, `espn`, `espn_sri_lanka`, and `pcb` are blocked by bot protection; `flashscore`, `livescore`, `asian_cricket`, and `zimbabwe_cricket` are fully client-rendered and would need a real browser to scrape.
- **Generic sources** - the other 18 sources (ICC, NBA, NFL, MLB, ATP, WTA, and cricket boards like ECB, NZC, Cricket South Africa, Cricket West Indies, Cricket Ireland, CricTotal) use a generic heuristic scraper. Results from these are low-confidence and dates are often "TBD".

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

Parallelism is internal to the orchestrator. `EventOrchestrator.run()` takes no arguments; it calls `scrape_all(max_workers=5)`. To change the worker count, edit the `scrape_all` call inside `run()` in `main.py`:

```python
all_events = self.scrape_all(max_workers=5)  # Increase for faster scraping
```

## Output

### Excel Columns

Events are written to `output/sports_events_[timestamp].xlsx` with these 8 columns:

| Column | Description |
|--------|-------------|
| Sport | Sport type (Cricket, Football, etc.) |
| Event | Match/Event name |
| Broadcasting Partner | Channel or broadcaster |
| Event Date | Date and time of event |
| Location | Event venue/city |
| Teams | Participating teams |
| Source | Which website the event came from |
| Timestamp | When the row was added to the file |

Duplicates are removed within a run; each run produces its own independent file.

### Logs

Logs are saved to:
- Scraper log: `logs/scraper.log` (single file, UTF-8; also printed to the console)
- Task Scheduler logs: `logs/scheduler_YYYY-MM-DD_HHMM.log`

## Troubleshooting

### Issue: "No events in the Excel file"

**Solutions**:
1. Check `logs/scraper.log` for errors
2. Run `python test_scrapers.py` to see which scrapers work
3. Generic-scraper sources often return few or no usable events - the dedicated `cricbuzz` and `bbc_sport` scrapers are the reliable ones

### Issue: "Excel file won't save / permission denied"

**Solution**: Close `output/sports_events_[timestamp].xlsx` in Excel before running the scraper - an open workbook is locked for writing.

### Issue: "Task Scheduler task fails silently"

**Solution**:
1. Check `logs/scheduler_*.log` for error details
2. Run `scheduler.bat` manually to see errors
3. If the log notes it fell back to system Python, run `setup.bat` to (re)create the virtual environment

### Issue: "Website returns 403 or 429 errors"

**Solution**:
- Increase delay between requests in `config/config.py`:
  ```python
  REQUEST_DELAY = 5  # Increase from 2 to 5 seconds
  ```
- Some sites block automated requests entirely (this is why `espn`, `espn_cricinfo`, `flashscore`, and `livescore` are disabled in `sources.json`). Consider using their APIs instead.

## Scaling & Maintenance

### Add New Sports Websites

1. **If site has available API**: Use it directly (faster, more reliable)
2. **For web scraping**:
   - Add an entry to `config/sources.json` with `id`, `name`, `url`, `sports`, `enabled`, and `scraper_type`
   - An unknown `scraper_type` automatically falls back to the generic heuristic scraper
   - For better results, create a custom scraper in `scrapers/` (inherit from `BaseScraper`), implement `_scrape()` (the base class's `scrape()` wraps it with error handling and logging), and add it to the `SCRAPER_CLASSES` dict in `scraper_factory.py`

### Performance Optimization

- Increase `max_workers` in the `scrape_all` call inside `main.py` for faster parallel scraping
- Use caching to skip redundant scrapes within 24 hours
- Disable sources with rate-limiting issues

### Website Structure Changes

Sports websites frequently update their HTML structure. If scraping stops working:

1. Run `python test_scrapers.py` - the offline fixture tests catch parser regressions for the dedicated scrapers
2. Check `logs/scraper.log` for parse errors
3. Update CSS selectors in the relevant scraper
4. Test with `python main.py`

## Dependencies

- **beautifulsoup4**: HTML parsing
- **requests**: HTTP requests with retries
- **openpyxl**: Excel file writing

That's the full list - `requirements.txt` contains nothing else.

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
3. Run the test suite: `python test_scrapers.py`

## License

Private use. Respect website terms of service when scraping.
