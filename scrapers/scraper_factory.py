"""
Scraper Factory
Dynamically creates scrapers based on configuration
"""
import json
from urllib.parse import urlparse
from config.config import SOURCES_FILE
from scrapers.espn_cricinfo_scraper import ESPNCricinfoScraper
from scrapers.bbc_sport_scraper import BBCSportScraper
from scrapers.flashscore_scraper import FlashscoreScraper
from scrapers.cricbuzz_scraper import CricbuzzScraper
from scrapers.generic_scraper import GenericScraper, _SPORT_KEYWORDS
from utils.logger import logger

# Mapping of scraper types to classes
SCRAPER_CLASSES = {
    "espn_cricinfo": ESPNCricinfoScraper,
    "bbc_sport": BBCSportScraper,
    "flashscore": FlashscoreScraper,
    "cricbuzz": CricbuzzScraper,
    "generic": GenericScraper,
}

def create_scraper_for_url(url, sport=None):
    """
    Build a scraper for one manually-entered URL.

    Always uses GenericScraper: the dedicated scrapers hardcode their own
    URLs, so routing an arbitrary link to them would silently ignore it.

    Args:
        url (str): Page to scrape ("https://" is assumed if no scheme given)
        sport (str): Sport label for the events; auto-detected per event
                     via keyword matching when omitted

    Returns:
        GenericScraper
    """
    if "://" not in url:
        url = "https://" + url

    domain = urlparse(url).netloc.lower()
    if domain.startswith("www."):
        domain = domain[4:]
    source_id = "manual_" + (domain.split(".")[0] or "url")

    sports = [sport] if sport else list(_SPORT_KEYWORDS.keys())
    logger.info(f"Manual URL scrape (generic heuristic, low confidence): {url}")
    return GenericScraper(source_id, url, sports)

def load_scrapers_from_config():
    """
    Load all enabled scrapers from configuration file.

    Returns:
        list: List of scraper instances
    """
    scrapers = []

    try:
        with open(SOURCES_FILE, "r", encoding="utf-8") as f:
            config = json.load(f)
    except Exception as e:
        logger.error(f"Failed to read sources config {SOURCES_FILE}: {e}")
        return scrapers

    for source in config.get("sources", []):
        source_id = source.get("id")
        try:
            if not source_id:
                logger.warning(f"Skipping source with no 'id': {source}")
                continue

            if not source.get("enabled", True):
                reason = source.get("disabled_reason", "")
                logger.info(f"Skipping disabled source: {source_id}" + (f" ({reason})" if reason else ""))
                continue

            url = source.get("url")
            sports = source.get("sports", [])
            scraper_type = source.get("scraper_type", "generic")
            scraper_class = SCRAPER_CLASSES.get(scraper_type)

            if scraper_class and scraper_class is not GenericScraper:
                scraper = scraper_class()
            else:
                if not url:
                    logger.warning(f"Skipping source {source_id}: no 'url' for generic scraping")
                    continue
                if not scraper_class:
                    logger.info(
                        f"No dedicated scraper for type '{scraper_type}' ({source_id}) — "
                        "using GenericScraper (heuristic, low confidence)"
                    )
                scraper = GenericScraper(source_id, url, sports)

            scrapers.append(scraper)
            logger.debug(f"Loaded scraper: {source_id}")
        except Exception as e:
            logger.error(f"Failed to load scraper {source_id or '<unknown>'}: {e}")

    logger.info(f"Loaded {len(scrapers)} scrapers")
    return scrapers
