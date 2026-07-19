"""
Generic Scraper
Fallback scraper for sources without specific implementation
"""
from bs4 import BeautifulSoup
from scrapers.base_scraper import BaseScraper
from utils.logger import logger

class GenericScraper(BaseScraper):
    """Generic scraper for sources without specific implementation"""
    
    def __init__(self, source_id, source_url, sports):
        super().__init__(source_id, source_url, sports)
    
    def scrape(self):
        """
        Generic scraping - attempts to find event-like elements.
        Returns minimal event data.
        """
        events = []
        try:
            logger.info(f"Scraping {self.source_id} (generic mode)...")
            
            response = self.fetch_page(self.source_url)
            
            if not response:
                logger.warning(f"Failed to fetch {self.source_url}")
                return events
            
            soup = BeautifulSoup(response.content, "html.parser")
            
            # Generic approach: find links that might be events
            links = soup.find_all("a", limit=10)
            
            for link in links:
                try:
                    text = link.get_text(strip=True)
                    href = link.get("href", "")
                    
                    # Skip navigation and empty links
                    if len(text) < 5 or not text or not href:
                        continue
                    
                    # Skip common navigation patterns
                    if any(x in text.lower() for x in ["home", "about", "contact", "signup", "login"]):
                        continue
                    
                    event = self.normalize_event(
                        sport=self.sports[0] if self.sports else "Sports",
                        event_name=text[:100],  # Limit length
                        broadcaster=self.source_id,
                        event_date="TBD",
                        location="TBD",
                        teams=text[:50]
                    )
                    events.append(event)
                except Exception as e:
                    logger.debug(f"Error parsing link: {e}")
                    continue
            
            logger.info(f"Found {len(events)} potential events from {self.source_id}")
        except Exception as e:
            logger.error(f"Error scraping {self.source_id}: {e}")
        
        return events
