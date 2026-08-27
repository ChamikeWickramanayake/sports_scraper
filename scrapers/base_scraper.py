"""
Base Scraper Class
All specific scrapers inherit from this class
"""
import requests
import time
import random
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from config.config import (
    USER_AGENTS,
    SCRAPER_TIMEOUT,
    SCRAPER_RETRY_ATTEMPTS,
    SCRAPER_RETRY_DELAY,
    REQUEST_DELAY,
)
from utils.logger import logger

class BaseScraper(ABC):
    """Abstract base class for all sport scrapers"""
    
    def __init__(self, source_id, source_url, sports):
        """
        Initialize scraper.
        
        Args:
            source_id (str): Unique identifier for source
            source_url (str): Base URL of the source
            sports (list): Sports this source covers
        """
        self.source_id = source_id
        self.source_url = source_url
        self.sports = sports
        self.session = requests.Session()
        self._setup_session()
    
    def _setup_session(self):
        """Setup requests session with headers"""
        user_agent = random.choice(USER_AGENTS)
        self.session.headers.update(
            {
                "User-Agent": user_agent,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Referer": self.source_url,
                "Connection": "keep-alive",
            }
        )
    
    def fetch_page(self, url, timeout=SCRAPER_TIMEOUT):
        """
        Fetch a web page with retry logic.
        
        Args:
            url (str): URL to fetch
            timeout (int): Request timeout in seconds
            
        Returns:
            requests.Response or None: Response object or None if failed
        """
        for attempt in range(SCRAPER_RETRY_ATTEMPTS):
            try:
                logger.debug(f"Fetching {url} (attempt {attempt + 1})")
                response = self.session.get(url, timeout=timeout)
                response.raise_for_status()
                time.sleep(REQUEST_DELAY)  # Be respectful to the server
                return response
            except requests.RequestException as e:
                logger.warning(f"Attempt {attempt + 1} failed: {e}")
                if attempt < SCRAPER_RETRY_ATTEMPTS - 1:
                    time.sleep(SCRAPER_RETRY_DELAY)
                else:
                    logger.error(f"Failed to fetch {url} after {SCRAPER_RETRY_ATTEMPTS} attempts")
                    return None

    def scrape(self):
        """
        Scrape events from the source, with failures made visible.

        Wraps the subclass _scrape() so that exceptions and empty results
        are always logged instead of silently producing an empty list.

        Returns:
            list: List of event dictionaries (see _scrape).
        """
        try:
            events = self._scrape() or []
        except Exception:
            logger.error(f"{self.source_id}: scrape failed with an unexpected error", exc_info=True)
            return []

        if not events:
            logger.warning(
                f"{self.source_id}: 0 events scraped from {self.source_url} — "
                "fetch failed or page structure may have changed"
            )
        else:
            logger.info(f"{self.source_id}: scraped {len(events)} events")
        return events

    @abstractmethod
    def _scrape(self):
        """
        Scrape events from the source.
        Must be implemented by subclasses.

        Returns:
            list: List of event dictionaries with keys:
                - sport (str): Sport name
                - event_name (str): Event or match name
                - broadcaster (str): Broadcasting partner
                - event_date (str): Event date, ISO %Y-%m-%d or "TBD"
                - location (str): Event location
                - teams (str): Teams/players involved
                - source (str): Source URL or ID
        """
        pass

    @staticmethod
    def to_iso_date(value):
        """
        Normalize a date value to ISO %Y-%m-%d.

        Args:
            value: Epoch milliseconds (int or numeric str) or an ISO-like
                   date string ("2026-08-27", "2026-08-27T18:30:00Z", ...).

        Returns:
            str: "YYYY-MM-DD", or "TBD" if the value can't be interpreted.
        """
        if value is None:
            return "TBD"
        try:
            if isinstance(value, (int, float)) or (isinstance(value, str) and value.isdigit()):
                ms = float(value)
                if ms > 1e11:  # epoch milliseconds
                    ms /= 1000.0
                return datetime.fromtimestamp(ms, tz=timezone.utc).strftime("%Y-%m-%d")
            text = str(value).strip()
            # ISO date or datetime prefix
            candidate = text[:10]
            datetime.strptime(candidate, "%Y-%m-%d")
            return candidate
        except (ValueError, OverflowError, OSError):
            return "TBD"

    def normalize_event(self, sport, event_name, broadcaster, event_date, location, teams=""):
        """
        Normalize event data.
        
        Args:
            sport (str): Sport name
            event_name (str): Event/match name
            broadcaster (str): Broadcasting partner
            event_date (str): Event date (ISO format or parseable)
            location (str): Event location
            teams (str): Teams involved
            
        Returns:
            dict: Normalized event
        """
        return {
            "sport": str(sport).strip() if sport else "",
            "event_name": str(event_name).strip() if event_name else "",
            "broadcaster": str(broadcaster).strip() if broadcaster else "",
            "event_date": str(event_date).strip() if event_date else "",
            "location": str(location).strip() if location else "",
            "teams": str(teams).strip() if teams else "",
            "source": self.source_id,
        }
