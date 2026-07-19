"""
Scraper Factory
Dynamically creates scrapers based on configuration
"""
import json
from config.config import SOURCES_FILE
from scrapers.base_scraper import BaseScraper
from scrapers.espn_cricinfo_scraper import ESPNCricinfoScraper
from scrapers.bbc_sport_scraper import BBCSportScraper
from scrapers.flashscore_scraper import FlashscoreScraper
from scrapers.cricbuzz_scraper import CricbuzzScraper
from scrapers.generic_scraper import GenericScraper
from utils.logger import logger

# Mapping of scraper types to classes
SCRAPER_CLASSES = {
    "espn_cricinfo": ESPNCricinfoScraper,
    "bbc_sport": BBCSportScraper,
    "flashscore": FlashscoreScraper,
    "cricbuzz": CricbuzzScraper,
    "generic": GenericScraper,
}

def get_scraper(source_id, source_url=None, sports=None):
    """
    Factory function to get the right scraper.
    
    Args:
        source_id (str): Source identifier
        source_url (str): Source URL (optional, used for generic scrapers)
        sports (list): Sports list (optional, used for generic scrapers)
        
    Returns:
        BaseScraper: Appropriate scraper instance
    """
    scraper_class = SCRAPER_CLASSES.get(source_id)
    
    if scraper_class and scraper_class != GenericScraper:
        try:
            return scraper_class()
        except Exception as e:
            logger.warning(f"Failed to instantiate {source_id}: {e}, falling back to generic")
    
    # Fallback to generic scraper
    if source_url and sports:
        return GenericScraper(source_id, source_url, sports)
    else:
        logger.error(f"Cannot create scraper for {source_id}: missing URL or sports")
        return None

def load_scrapers_from_config():
    """
    Load all enabled scrapers from configuration file.
    
    Returns:
        list: List of scraper instances
    """
    scrapers = []
    
    try:
        with open(SOURCES_FILE, "r") as f:
            config = json.load(f)
        
        for source in config.get("sources", []):
            if not source.get("enabled", True):
                logger.debug(f"Skipping disabled source: {source['id']}")
                continue
            
            scraper_type = source.get("scraper_type", "generic")
            
            if scraper_type in SCRAPER_CLASSES:
                scraper_class = SCRAPER_CLASSES[scraper_type]
                try:
                    if scraper_type == "generic":
                        scraper = scraper_class(
                            source["id"],
                            source["url"],
                            source.get("sports", [])
                        )
                    else:
                        scraper = scraper_class()
                    scrapers.append(scraper)
                    logger.debug(f"Loaded scraper: {source['id']}")
                except Exception as e:
                    logger.error(f"Failed to load scraper {source['id']}: {e}")
            else:
                # Use generic scraper
                scraper = GenericScraper(
                    source["id"],
                    source["url"],
                    source.get("sports", [])
                )
                scrapers.append(scraper)
                logger.debug(f"Loaded generic scraper: {source['id']}")
    
    except Exception as e:
        logger.error(f"Failed to load scrapers from config: {e}")
    
    logger.info(f"Loaded {len(scrapers)} scrapers")
    return scrapers
