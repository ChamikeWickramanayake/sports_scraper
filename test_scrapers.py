"""
Test Script for Sports Events Scraper
Tests individual scrapers without requiring Google Sheets setup
"""
import json
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from scrapers.scraper_factory import load_scrapers_from_config
from config.config import CACHE_DIR
from utils.logger import logger

def test_scrapers(max_scrapers=3):
    """Test individual scrapers"""
    logger.info("=" * 60)
    logger.info("Testing Sports Events Scrapers")
    logger.info("=" * 60)
    
    scrapers = load_scrapers_from_config()
    
    if not scrapers:
        logger.error("No scrapers loaded!")
        return False
    
    logger.info(f"Loaded {len(scrapers)} scrapers, testing first {max_scrapers}...")
    
    results = {}
    for i, scraper in enumerate(scrapers[:max_scrapers]):
        try:
            logger.info(f"\n[{i+1}/{max_scrapers}] Testing {scraper.source_id}...")
            events = scraper.scrape()
            
            results[scraper.source_id] = {
                "status": "success",
                "events_count": len(events),
                "sample": events[:2] if events else []
            }
            
            logger.info(f"✓ {scraper.source_id}: Found {len(events)} events")
            
            # Print sample event
            if events:
                logger.debug(f"  Sample: {json.dumps(events[0], indent=2)}")
        
        except Exception as e:
            logger.error(f"✗ {scraper.source_id}: {e}")
            results[scraper.source_id] = {
                "status": "failed",
                "error": str(e)
            }
    
    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("Test Summary")
    logger.info("=" * 60)
    
    success_count = sum(1 for r in results.values() if r["status"] == "success")
    failed_count = sum(1 for r in results.values() if r["status"] == "failed")
    total_events = sum(r.get("events_count", 0) for r in results.values())
    
    logger.info(f"Successful: {success_count}/{len(results)}")
    logger.info(f"Failed: {failed_count}/{len(results)}")
    logger.info(f"Total events found: {total_events}")
    
    # Save results to file
    results_file = CACHE_DIR / "test_results.json"
    try:
        with open(results_file, "w") as f:
            json.dump(results, f, indent=2, default=str)
        logger.info(f"\nResults saved to: {results_file}")
    except Exception as e:
        logger.warning(f"Could not save results: {e}")
    
    return failed_count == 0

def test_excel_export():
    """Test Excel export (optional)"""
    logger.info("\n" + "=" * 60)
    logger.info("Testing Excel Export")
    logger.info("=" * 60)
    
    try:
        from utils.excel_export import ExcelExporter
        from config.config import EXCEL_FILE
        
        exporter = ExcelExporter()
        
        # Test with sample data
        sample_events = [
            {
                "sport": "Cricket",
                "event_name": "Test Match",
                "broadcaster": "ESPN",
                "event_date": "2026-08-01",
                "location": "India",
                "teams": "India vs Australia",
                "source": "test"
            }
        ]
        
        exporter.append_events(sample_events)
        logger.info(f"✓ Successfully created/updated Excel file: {EXCEL_FILE}")
        return True
    
    except Exception as e:
        logger.warning(f"✗ Excel export test failed: {e}")
        return False

def main():
    """Run all tests"""
    logger.info("\n")
    
    # Test scrapers
    scrapers_ok = test_scrapers(max_scrapers=3)
    
    # Test Excel export
    excel_ok = test_excel_export()
    
    # Final summary
    logger.info("\n" + "=" * 60)
    logger.info("Test Complete")
    logger.info("=" * 60)
    
    if scrapers_ok:
        logger.info("✓ Scraper tests PASSED")
    else:
        logger.warning("⚠ Some scraper tests FAILED (expected for new sites)")
    
    if excel_ok:
        logger.info("✓ Excel export PASSED")
    else:
        logger.warning("⚠ Excel export FAILED")
    
    logger.info("\nNext steps:")
    logger.info("1. Run: python main.py")
    logger.info("2. Check output/sports_events.xlsx for exported events")
    logger.info("\n")

if __name__ == "__main__":
    main()
