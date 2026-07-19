"""
Main Orchestrator
Coordinates scraping, deduplication, and Excel export
"""
import os
import json
from pathlib import Path
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
from config.config import CACHE_DIR, MIN_EVENT_DAYS_AHEAD, MAX_EVENT_DAYS_AHEAD
from scrapers.scraper_factory import load_scrapers_from_config
from utils.excel_export import ExcelExporter
from utils.logger import logger

class EventOrchestrator:
    """Orchestrates the entire scraping and syncing process"""
    
    def __init__(self):
        """Initialize orchestrator"""
        self.cache_file = CACHE_DIR / "events_cache.json"
        self.events_cache = {}
        self.all_events = []
    
    def load_cache(self):
        """Load events from cache if available"""
        try:
            if self.cache_file.exists():
                with open(self.cache_file, "r") as f:
                    cache = json.load(f)
                
                # Check if cache is fresh
                cache_time = datetime.fromisoformat(cache.get("timestamp", ""))
                age_hours = (datetime.now() - cache_time).total_seconds() / 3600
                
                if age_hours < 24:
                    self.events_cache = cache.get("events", {})
                    logger.info(f"Loaded cache with {len(self.events_cache)} events (age: {age_hours:.1f}h)")
                    return True
        except Exception as e:
            logger.warning(f"Failed to load cache: {e}")
        
        return False
    
    def save_cache(self):
        """Save current events to cache"""
        try:
            cache = {
                "timestamp": datetime.now().isoformat(),
                "events": {k: v for k, v in self.events_cache.items()},
            }
            with open(self.cache_file, "w") as f:
                json.dump(cache, f, indent=2)
            logger.info(f"Saved cache with {len(self.events_cache)} events")
        except Exception as e:
            logger.error(f"Failed to save cache: {e}")
    
    def scrape_from_source(self, scraper):
        """
        Scrape events from a single source.
        
        Args:
            scraper: Scraper instance
            
        Returns:
            tuple: (source_id, events_list)
        """
        try:
            events = scraper.scrape()
            logger.info(f"{scraper.source_id}: scraped {len(events)} events")
            return (scraper.source_id, events)
        except Exception as e:
            logger.error(f"{scraper.source_id}: scraping failed: {e}")
            return (scraper.source_id, [])
    
    def scrape_all(self, max_workers=5):
        """
        Run all scrapers in parallel.
        
        Args:
            max_workers (int): Maximum concurrent scrapers
        """
        logger.info("Starting parallel scraping...")
        scrapers = load_scrapers_from_config()
        
        if not scrapers:
            logger.error("No scrapers loaded!")
            return
        
        all_events = []
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(self.scrape_from_source, scraper) for scraper in scrapers]
            
            for future in as_completed(futures):
                try:
                    source_id, events = future.result()
                    all_events.extend(events)
                except Exception as e:
                    logger.error(f"Error processing scraper result: {e}")
        
        logger.info(f"Total events scraped: {len(all_events)}")
        return all_events
    
    def filter_events(self, events):
        """
        Filter events by date range (exclude past events).
        
        Args:
            events (list): List of events to filter
            
        Returns:
            list: Filtered events
        """
        now = datetime.now()
        min_date = now + timedelta(days=MIN_EVENT_DAYS_AHEAD)
        max_date = now + timedelta(days=MAX_EVENT_DAYS_AHEAD)
        
        filtered = []
        for event in events:
            try:
                # Try to parse event date
                event_date_str = event.get("event_date", "")
                
                # Skip if date is "TBD" or empty
                if not event_date_str or event_date_str == "TBD":
                    filtered.append(event)
                    continue
                
                # Simple date parsing (try multiple formats)
                event_date = None
                for fmt in ["%Y-%m-%d", "%d-%m-%Y", "%Y-%m-%d %H:%M", "%d/%m/%Y"]:
                    try:
                        event_date = datetime.strptime(event_date_str.split()[0], fmt)
                        break
                    except:
                        continue
                
                if event_date and min_date <= event_date <= max_date:
                    filtered.append(event)
            except Exception as e:
                logger.debug(f"Error filtering event: {e}")
                filtered.append(event)  # Include if uncertain
        
        logger.info(f"Filtered events: {len(events)} → {len(filtered)}")
        return filtered
    
    def deduplicate_events(self, events):
        """
        Remove duplicate events based on key fields.
        
        Args:
            events (list): List of events
            
        Returns:
            list: Deduplicated events
        """
        seen = set()
        unique_events = []
        
        for event in events:
            # Create a key for deduplication
            key = (
                event.get("sport", "").lower(),
                event.get("event_name", "").lower(),
                event.get("event_date", "").lower(),
                event.get("location", "").lower(),
            )
            
            if key not in seen:
                seen.add(key)
                unique_events.append(event)
            else:
                logger.debug(f"Duplicate detected: {event.get('event_name')}")
        
        logger.info(f"Deduplicated: {len(events)} → {len(unique_events)}")
        return unique_events
    
    def run(self):
        """
        Execute the full workflow: scrape, deduplicate, filter, export to Excel.
        """
        logger.info("=" * 60)
        logger.info("Starting Sports Events Scraper")
        logger.info(f"Timestamp: {datetime.now().isoformat()}")
        logger.info("=" * 60)
        
        # Load cache
        self.load_cache()
        
        # Scrape all sources
        all_events = self.scrape_all(max_workers=5)
        
        # Filter by date range
        filtered_events = self.filter_events(all_events)
        
        # Deduplicate
        unique_events = self.deduplicate_events(filtered_events)
        
        # Save to cache
        self.events_cache = {str(i): e for i, e in enumerate(unique_events)}
        self.save_cache()
        
        # Export to Excel
        if unique_events:
            try:
                exporter = ExcelExporter()
                exporter.append_events(unique_events)
                logger.info("Successfully exported to Excel")
            except Exception as e:
                logger.error(f"Failed to export to Excel: {e}")
        
        logger.info("=" * 60)
        logger.info(f"Scraping completed. Processed {len(unique_events)} events.")
        logger.info("=" * 60)
        
        return unique_events

def main():
    """Entry point"""
    try:
        orchestrator = EventOrchestrator()
        orchestrator.run()
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    main()
