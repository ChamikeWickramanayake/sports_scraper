"""
Flashscore Scraper
Multi-sport live scores and fixtures
"""
from bs4 import BeautifulSoup
from scrapers.base_scraper import BaseScraper
from utils.logger import logger

class FlashscoreScraper(BaseScraper):
    """Scraper for Flashscore events"""
    
    def __init__(self):
        super().__init__(
            source_id="flashscore",
            source_url="https://www.flashscore.com",
            sports=["Football", "Basketball", "Tennis", "Hockey", "Baseball", "Cricket"]
        )
    
    def scrape(self):
        """Scrape upcoming events from Flashscore"""
        events = []
        try:
            logger.info("Scraping Flashscore...")
            
            url = "https://www.flashscore.com/"
            response = self.fetch_page(url)
            
            if not response:
                logger.warning("Failed to fetch Flashscore page")
                return events
            
            soup = BeautifulSoup(response.content, "html.parser")
            
            # Find match events
            matches = soup.find_all("div", class_="event")
            
            for match in matches[:20]:  # Limit to 20 events
                try:
                    event_text = match.get_text(strip=True)
                    
                    # Parse event details
                    teams_elem = match.find("span", class_="teams")
                    time_elem = match.find("span", class_="time")
                    sport_elem = match.find("span", class_="sport")
                    
                    teams = teams_elem.get_text(strip=True) if teams_elem else "TBD"
                    time = time_elem.get_text(strip=True) if time_elem else "TBD"
                    sport = sport_elem.get_text(strip=True) if sport_elem else "Sports"
                    
                    event = self.normalize_event(
                        sport=sport,
                        event_name=teams,
                        broadcaster="Flashscore",
                        event_date=time,
                        location="TBD",
                        teams=teams
                    )
                    events.append(event)
                except Exception as e:
                    logger.debug(f"Error parsing Flashscore event: {e}")
                    continue
            
            logger.info(f"Found {len(events)} events from Flashscore")
        except Exception as e:
            logger.error(f"Error scraping Flashscore: {e}")
        
        return events
