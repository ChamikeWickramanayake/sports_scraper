"""
Configuration settings for Sports Events Scraper
"""
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
LOGS_DIR = PROJECT_ROOT / "logs"
CACHE_DIR = PROJECT_ROOT / "cache"
CONFIG_DIR = PROJECT_ROOT / "config"

# Ensure directories exist
LOGS_DIR.mkdir(exist_ok=True)
CACHE_DIR.mkdir(exist_ok=True)

# Logging configuration
LOG_FILE = LOGS_DIR / "scraper.log"
LOG_LEVEL = "INFO"

# Excel export configuration
OUTPUT_DIR = PROJECT_ROOT / "output"
OUTPUT_DIR.mkdir(exist_ok=True)
# Each run writes its own file: <prefix>_<YYYY-MM-DD_HHMMSS>.xlsx
EXCEL_FILE_PREFIX = "sports_events"

# Scraper configuration
SCRAPER_TIMEOUT = 30  # seconds
SCRAPER_RETRY_ATTEMPTS = 3
SCRAPER_RETRY_DELAY = 5  # seconds
REQUEST_DELAY = 2  # seconds between requests per scraper

# User agents for web requests
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0",
]

# Data configuration
CACHE_EXPIRY_HOURS = 24  # Cache data for 24 hours
MIN_EVENT_DAYS_AHEAD = 0  # Include events from today onwards (0) or future only (1)
MAX_EVENT_DAYS_AHEAD = 365  # Include events up to 1 year ahead

# Excel columns (base columns; ExcelExporter appends Teams, Source, Timestamp)
EXCEL_COLUMNS = [
    "Sport",
    "Event",
    "Broadcasting Partner",
    "Event Date",
    "Location",
]

# Deduplication settings
DEDUP_TOLERANCE_HOURS = 24  # Events within 24 hours of each other are considered duplicates
DEDUP_FIELDS = ("sport", "event_name", "event_date", "location")  # Fields to match for deduplication

# Sources configuration file
SOURCES_FILE = CONFIG_DIR / "sources.json"
