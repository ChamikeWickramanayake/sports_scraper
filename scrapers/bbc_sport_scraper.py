"""
BBC Sport Scraper
Extracts sports events from BBC Sport
"""
from bs4 import BeautifulSoup
from scrapers.base_scraper import BaseScraper
from utils.logger import logger

class BBCSportScraper(BaseScraper):
    """Scraper for BBC Sport events"""
    
    def __init__(self):
        super().__init__(
            source_id="bbc_sport",
            source_url="https://www.bbc.com/sport",
            sports=["Football", "Tennis", "Cricket", "Rugby", "Golf", "Basketball"]
        )
    
    def scrape(self):
        """Scrape upcoming events from BBC Sport"""
        events = []
        try:
            logger.info("Scraping BBC Sport...")
            
            url = "https://www.bbc.com/sport/live"
            response = self.fetch_page(url)
            
            if not response:
                logger.warning("Failed to fetch BBC Sport page")
                return events
            
            soup = BeautifulSoup(response.content, "html.parser")
            
            # Find event cards
            event_cards = soup.find_all("a", class_=["sc-4fedabbc-3"])
            
            for card in event_cards[:15]:  # Limit to 15 events
                try:
                    title = card.get_text(strip=True)
                    link = card.get("href", "")
                    
                    # Extract sport from URL/title
                    sport = "Sports"
                    if "football" in link.lower():
                        sport = "Football"
                    elif "tennis" in link.lower():
                        sport = "Tennis"
                    elif "cricket" in link.lower():
                        sport = "Cricket"
                    elif "rugby" in link.lower():
                        sport = "Rugby"
                    
                    event = self.normalize_event(
                        sport=sport,
                        event_name=title,
                        broadcaster="BBC Sport",
                        event_date="TBD",
                        location="TBD",
                        teams=title
                    )
                    events.append(event)
                except Exception as e:
                    logger.debug(f"Error parsing BBC card: {e}")
                    continue
            
            logger.info(f"Found {len(events)} events from BBC Sport")
        except Exception as e:
            logger.error(f"Error scraping BBC Sport: {e}")
        
        return events
