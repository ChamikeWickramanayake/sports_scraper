"""
ESPN Cricinfo Scraper — disabled stub

ESPN Cricinfo sits behind Akamai bot protection that fingerprints the TLS
stack: both the HTML pages and the hs-consumer-api JSON endpoint return
403 to non-browser clients even with full browser headers (verified
2026-08 across two different TLS stacks). Scraping it would need real
browser automation, which this project deliberately avoids.

The source is disabled in config/sources.json; cricket coverage comes from
Cricbuzz (plus BBC Sport cricket fixtures). If re-enabled, this stub makes
one fetch attempt and logs loudly instead of failing silently.
"""
from scrapers.base_scraper import BaseScraper
from utils.logger import logger

class ESPNCricinfoScraper(BaseScraper):
    """Stub scraper for ESPN Cricinfo (site blocks non-browser clients)"""

    FIXTURES_URL = "https://www.espncricinfo.com/live-cricket-match-schedule-fixtures"

    def __init__(self):
        super().__init__(
            source_id="espn_cricinfo",
            source_url="https://www.espncricinfo.com",
            sports=["Cricket"]
        )

    def _scrape(self):
        logger.warning(
            "espn_cricinfo: ESPN Cricinfo blocks non-browser clients via Akamai TLS "
            "fingerprinting (verified 2026-08) — expect 403. Cricket coverage comes "
            "from cricbuzz instead."
        )
        response = self.fetch_page(self.FIXTURES_URL)
        if response is not None:
            logger.warning(
                "espn_cricinfo: unexpectedly received a page, but no parser is "
                "implemented for the current site structure — returning 0 events"
            )
        return []
