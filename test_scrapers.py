"""
Test Script for Sports Events Scraper
Tests individual scrapers and the Excel export
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

            # A scrape that yields nothing is NOT a success — it usually means
            # the fetch failed or the page structure changed.
            if events:
                status = "success"
                logger.info(f"✓ {scraper.source_id}: Found {len(events)} events")
                logger.debug(f"  Sample: {json.dumps(events[0], indent=2)}")
            else:
                status = "no_events"
                logger.warning(f"⚠ {scraper.source_id}: scrape returned 0 events")

            results[scraper.source_id] = {
                "status": status,
                "events_count": len(events),
                "sample": events[:2] if events else []
            }

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
    no_events_count = sum(1 for r in results.values() if r["status"] == "no_events")
    failed_count = sum(1 for r in results.values() if r["status"] == "failed")
    total_events = sum(r.get("events_count", 0) for r in results.values())

    logger.info(f"Successful (with events): {success_count}/{len(results)}")
    logger.info(f"Returned 0 events: {no_events_count}/{len(results)}")
    logger.info(f"Failed: {failed_count}/{len(results)}")
    logger.info(f"Total events found: {total_events}")

    # Save results to file
    results_file = CACHE_DIR / "test_results.json"
    try:
        with open(results_file, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, default=str, ensure_ascii=False)
        logger.info(f"\nResults saved to: {results_file}")
    except Exception as e:
        logger.warning(f"Could not save results: {e}")

    return failed_count == 0 and success_count > 0

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

def test_offline_parsing():
    """
    Parse saved HTML fixtures so site-structure regressions in the dedicated
    scrapers fail here instead of silently yielding 0 events in production.
    """
    logger.info("\n" + "=" * 60)
    logger.info("Testing Offline Fixture Parsing")
    logger.info("=" * 60)

    from scrapers.cricbuzz_scraper import CricbuzzScraper
    from scrapers.bbc_sport_scraper import BBCSportScraper

    fixtures = Path(__file__).parent / "tests" / "fixtures"
    ok = True

    cricbuzz_file = fixtures / "cricbuzz_schedule.html"
    if cricbuzz_file.exists():
        html = cricbuzz_file.read_text(encoding="utf-8")
        # Fixed date floor: fixture snapshots age, live filtering uses today
        events = CricbuzzScraper()._parse_flight_data(html, today="2000-01-01")
        dated = sum(1 for e in events if e["event_date"] != "TBD")
        if events and dated:
            logger.info(f"✓ Cricbuzz fixture: parsed {len(events)} matches ({dated} with dates)")
        else:
            logger.error(f"✗ Cricbuzz fixture: parsed {len(events)} matches, {dated} with dates")
            ok = False
    else:
        logger.warning("⚠ Cricbuzz fixture missing, skipping")

    bbc_file = fixtures / "bbc_football_fixtures.html"
    if bbc_file.exists():
        html = bbc_file.read_text(encoding="utf-8")
        events = BBCSportScraper()._parse_initial_data(html, "Football", set())
        dated = sum(1 for e in events if e["event_date"] != "TBD")
        if events and dated:
            logger.info(f"✓ BBC fixture: parsed {len(events)} fixtures ({dated} with dates)")
        else:
            logger.error(f"✗ BBC fixture: parsed {len(events)} fixtures, {dated} with dates")
            ok = False
    else:
        logger.warning("⚠ BBC fixture missing, skipping")

    return ok

def main():
    """Run all tests"""
    logger.info("\n")

    # Test fixture parsing first (fast, no network)
    parsing_ok = test_offline_parsing()

    # Test scrapers
    scrapers_ok = test_scrapers(max_scrapers=3)

    # Test Excel export
    excel_ok = test_excel_export()
    
    # Final summary
    logger.info("\n" + "=" * 60)
    logger.info("Test Complete")
    logger.info("=" * 60)

    if parsing_ok:
        logger.info("✓ Offline fixture parsing PASSED")
    else:
        logger.warning("⚠ Offline fixture parsing FAILED (site parsers are broken)")

    if scrapers_ok:
        logger.info("✓ Scraper tests PASSED")
    else:
        logger.warning("⚠ Some scraper tests FAILED or returned no events")

    if excel_ok:
        logger.info("✓ Excel export PASSED")
    else:
        logger.warning("⚠ Excel export FAILED")

    logger.info("\nNext steps:")
    logger.info("1. Run: python main.py")
    logger.info("2. Check output/sports_events.xlsx for exported events")
    logger.info("\n")

    return parsing_ok and scrapers_ok and excel_ok

if __name__ == "__main__":
    sys.exit(0 if main() else 1)
