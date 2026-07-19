"""
ESPN Cricinfo Scraper
Extracts cricket events, series, and fixtures
"""
from bs4 import BeautifulSoup
from datetime import datetime
from scrapers.base_scraper import BaseScraper
from utils.logger import logger

class ESPNCricinfoScraper(BaseScraper):
    """Scraper for ESPN Cricinfo cricket events"""
    
    def __init__(self):
        super().__init__(
            source_id="espn_cricinfo",
            source_url="https://www.espncricinfo.com",
            sports=["Cricket"]
        )
    
    def scrape(self):
        """Scrape upcoming cricket matches from Cricinfo"""
        events = []
        try:
            logger.info("Scraping ESPN Cricinfo...")
            
            # Scrape upcoming fixtures page
            url = "https://www.espncricinfo.com/ci/engine/current/match/index.html"
            response = self.fetch_page(url)
            
            if not response:
                logger.warning("Failed to fetch Cricinfo page")
                return events
            
            soup = BeautifulSoup(response.content, "html.parser")
            
            # Find match rows (structure may vary)
            match_rows = soup.find_all("tr", class_=["row-odd", "row-even"])
            
            for row in match_rows[:10]:  # Limit to 10 matches
                try:
                    cols = row.find_all("td")
                    if len(cols) >= 4:
                        match_name = cols[0].get_text(strip=True)
                        date_str = cols[1].get_text(strip=True)
                        location = cols[2].get_text(strip=True)
                        status = cols[3].get_text(strip=True)
                        
                        event = self.normalize_event(
                            sport="Cricket",
                            event_name=match_name,
                            broadcaster="ESPN Cricinfo",
                            event_date=date_str,
                            location=location,
                            teams=match_name
                        )
                        events.append(event)
                except Exception as e:
                    logger.debug(f"Error parsing row: {e}")
                    continue
            
            logger.info(f"Found {len(events)} cricket events from Cricinfo")
        except Exception as e:
            logger.error(f"Error scraping Cricinfo: {e}")
        
        return events
