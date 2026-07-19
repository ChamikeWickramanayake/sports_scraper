"""
Cricbuzz Scraper
Cricket events and fixtures
"""
from bs4 import BeautifulSoup
from scrapers.base_scraper import BaseScraper
from utils.logger import logger

class CricbuzzScraper(BaseScraper):
    """Scraper for Cricbuzz cricket events"""
    
    def __init__(self):
        super().__init__(
            source_id="cricbuzz",
            source_url="https://www.cricbuzz.com",
            sports=["Cricket"]
        )
    
    def scrape(self):
        """Scrape cricket events from Cricbuzz"""
        events = []
        try:
            logger.info("Scraping Cricbuzz...")
            
            url = "https://www.cricbuzz.com/cricket-schedule/upcoming-series"
            response = self.fetch_page(url)
            
            if not response:
                logger.warning("Failed to fetch Cricbuzz page")
                return events
            
            soup = BeautifulSoup(response.content, "html.parser")
            
            # Find match elements
            matches = soup.find_all("div", class_=["cb-scrd-itm", "cb-scrd-itms"])
            
            for match in matches[:15]:  # Limit to 15 events
                try:
                    match_title = match.find("a", class_="cb-scrd-itm-text")
                    date_elem = match.find("span", class_="cb-scrd-itm-date")
                    
                    if match_title:
                        title = match_title.get_text(strip=True)
                        date = date_elem.get_text(strip=True) if date_elem else "TBD"
                        
                        event = self.normalize_event(
                            sport="Cricket",
                            event_name=title,
                            broadcaster="Cricbuzz",
                            event_date=date,
                            location="TBD",
                            teams=title
                        )
                        events.append(event)
                except Exception as e:
                    logger.debug(f"Error parsing Cricbuzz match: {e}")
                    continue
            
            logger.info(f"Found {len(events)} cricket events from Cricbuzz")
        except Exception as e:
            logger.error(f"Error scraping Cricbuzz: {e}")
        
        return events
