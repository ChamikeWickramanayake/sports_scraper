"""
BBC Sport Scraper
Extracts sports fixtures from BBC Sport scores-fixtures pages

The fixtures are embedded server-side in window.__INITIAL_DATA__ as a
double-encoded JSON string. The keys directly under "data" are volatile
cache keys, so event objects are found by recursively walking the payload
for dicts that carry home/away/startDateTime.
"""
import json
import re
from datetime import datetime, timedelta
from scrapers.base_scraper import BaseScraper
from utils.logger import logger

# window.__INITIAL_DATA__="{\"data\":{...}}";  (a JS string literal)
_INITIAL_DATA = re.compile(r'window\.__INITIAL_DATA__="((?:[^"\\]|\\.)*)"')

class BBCSportScraper(BaseScraper):
    """Scraper for BBC Sport fixtures"""

    # URL path segment -> sport label
    FIXTURE_PAGES = {
        "https://www.bbc.com/sport/football/scores-fixtures": "Football",
        "https://www.bbc.com/sport/cricket/scores-fixtures": "Cricket",
    }
    LOOKAHEAD_DAYS = 2  # also fetch /{YYYY-MM-DD} for the next N days

    def __init__(self):
        super().__init__(
            source_id="bbc_sport",
            source_url="https://www.bbc.com/sport",
            sports=["Football", "Cricket"]
        )

    def _scrape(self):
        """Scrape upcoming fixtures from BBC Sport"""
        logger.info("Scraping BBC Sport...")
        events = []
        seen = set()

        for base_url, sport in self.FIXTURE_PAGES.items():
            urls = [base_url]
            today = datetime.now()
            for offset in range(1, self.LOOKAHEAD_DAYS + 1):
                day = (today + timedelta(days=offset)).strftime("%Y-%m-%d")
                urls.append(f"{base_url}/{day}")

            for url in urls:
                response = self.fetch_page(url)
                if not response:
                    logger.warning(f"bbc_sport: failed to fetch {url}")
                    continue
                page_events = self._parse_initial_data(response.text, sport, seen)
                events.extend(page_events)

        logger.info(f"Found {len(events)} events from BBC Sport")
        return events

    def _parse_initial_data(self, html, sport, seen):
        """Extract fixtures from the embedded __INITIAL_DATA__ JSON."""
        m = _INITIAL_DATA.search(html)
        if not m:
            logger.warning("bbc_sport: window.__INITIAL_DATA__ not found — page structure may have changed")
            return []

        try:
            # Unescape the JS string literal, then parse the JSON it contains
            payload = json.loads(json.loads('"' + m.group(1) + '"'))
        except ValueError as e:
            logger.warning(f"bbc_sport: failed to parse __INITIAL_DATA__: {e}")
            return []

        events = []
        for node in self._find_fixtures(payload):
            home = self._participant_name(node.get("home"))
            away = self._participant_name(node.get("away"))
            start = str(node.get("startDateTime") or "")
            if not (home and away and start):
                continue

            key = node.get("id") or node.get("urn") or (home, away, start[:10])
            if key in seen:
                continue
            seen.add(key)

            label = node.get("eventGroupingLabel") or ""
            venue = node.get("venue")
            if isinstance(venue, dict):
                venue = venue.get("name") or venue.get("fullName") or ""

            # Include teams in the name: the dedup key is (sport, name, date,
            # location), and the competition label alone collides for two
            # different matches in the same competition on the same day.
            matchup = f"{home} vs {away}"
            events.append(self.normalize_event(
                sport=sport,
                event_name=f"{matchup} ({label})" if label else matchup,
                broadcaster="BBC Sport",
                event_date=self.to_iso_date(start),
                location=venue or "",
                teams=f"{home} vs {away}"
            ))
        return events

    def _find_fixtures(self, node):
        """Recursively yield dicts that look like fixture events."""
        if isinstance(node, dict):
            if "home" in node and "away" in node and "startDateTime" in node:
                yield node
            else:
                for value in node.values():
                    yield from self._find_fixtures(value)
        elif isinstance(node, list):
            for item in node:
                yield from self._find_fixtures(item)

    @staticmethod
    def _participant_name(participant):
        """Pull a team/player name out of a home/away participant object."""
        if not isinstance(participant, dict):
            return ""
        for key in ("fullName", "shortName"):
            if participant.get(key):
                return str(participant[key])
        name = participant.get("name")
        if isinstance(name, dict):
            return str(name.get("fullName") or name.get("shortName") or "")
        if name:
            return str(name)
        return ""
