"""
Flashscore Scraper — disabled stub

Flashscore is fully client-rendered: the HTML served to non-browser clients
is an empty JS shell (verified 2026-08), and the underlying d.flashscore.com
data feeds require a JavaScript-generated x-fsign header. Scraping it would
need real browser automation, which this project deliberately avoids.

The source is disabled in config/sources.json. If re-enabled, this stub logs
loudly and returns no events instead of failing silently.
"""
from scrapers.base_scraper import BaseScraper
from utils.logger import logger

class FlashscoreScraper(BaseScraper):
    """Stub scraper for Flashscore (site is fully client-rendered)"""

    def __init__(self):
        super().__init__(
            source_id="flashscore",
            source_url="https://www.flashscore.com",
            sports=["Football", "Basketball", "Tennis", "Hockey", "Baseball", "Cricket"]
        )

    def _scrape(self):
        logger.warning(
            "flashscore: Flashscore is fully client-rendered and requires a browser "
            "to scrape (verified 2026-08) — returning 0 events without fetching"
        )
        return []
