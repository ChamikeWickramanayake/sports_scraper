"""
Cricbuzz Scraper
Cricket events and fixtures

The schedule page is a server-rendered Next.js app: match data is embedded in
RSC "flight" chunks (self.__next_f.push([1,"..."]) script calls) rather than
in the visible DOM, which is rendered client-side from those chunks. Parsing
the flight data is the only way to get dates/venues, and it is more stable
than Cricbuzz's hashed Tailwind CSS classes.
"""
import json
import re
from datetime import datetime, timezone
from bs4 import BeautifulSoup
from scrapers.base_scraper import BaseScraper
from utils.logger import logger

# Body of a JS string literal pushed as a flight chunk
_FLIGHT_CHUNK = re.compile(r'self\.__next_f\.push\(\[1,"((?:[^"\\]|\\.)*)"\]\)')
# JSON string value, escapes preserved
_JSTR = r'"((?:[^"\\]|\\.)*)"'


def _json_str(pattern, text):
    """Extract and unescape the first JSON string captured by pattern."""
    m = re.search(pattern, text)
    if not m:
        return ""
    try:
        return json.loads('"' + m.group(1) + '"')
    except ValueError:
        return m.group(1)


class CricbuzzScraper(BaseScraper):
    """Scraper for Cricbuzz cricket events"""

    # This single page carries INTERNATIONAL, LEAGUE, DOMESTIC and WOMEN sections
    SCHEDULE_URL = "https://www.cricbuzz.com/cricket-schedule/upcoming-series/international"

    def __init__(self):
        super().__init__(
            source_id="cricbuzz",
            source_url="https://www.cricbuzz.com",
            sports=["Cricket"]
        )

    def _scrape(self):
        """Scrape upcoming cricket matches from Cricbuzz"""
        logger.info("Scraping Cricbuzz...")

        response = self.fetch_page(self.SCHEDULE_URL)
        if not response:
            return []

        html = response.text
        events = self._parse_flight_data(html)

        if not events:
            logger.warning(
                "cricbuzz: flight-data parse yielded 0 matches — falling back to "
                "DOM anchors (degraded: no dates/venues)"
            )
            events = self._parse_dom_fallback(html)

        return events

    def _parse_flight_data(self, html, today=None):
        """Extract matches from the embedded Next.js RSC flight chunks.

        Args:
            html (str): Page HTML.
            today (str): ISO date floor for keeping matches (default: today UTC).
        """
        chunks = _FLIGHT_CHUNK.findall(html)
        if not chunks:
            return []

        decoded = []
        for chunk in chunks:
            try:
                decoded.append(json.loads('"' + chunk + '"'))
            except ValueError:
                continue
        # A match object can be split across two pushes, so parse the joined text
        payload = "".join(decoded)

        events = []
        seen_ids = set()
        if today is None:
            today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

        positions = [m.start() for m in re.finditer(r'"matchInfo":\{', payload)]
        for i, pos in enumerate(positions):
            end = positions[i + 1] if i + 1 < len(positions) else min(pos + 3000, len(payload))
            window = payload[pos:end]

            m = re.search(r'"matchId":(\d+)', window)
            match_id = m.group(1) if m else None
            if not match_id or match_id in seen_ids:
                continue

            series_name = _json_str(r'"seriesName":' + _JSTR, window)
            match_desc = _json_str(r'"matchDesc":' + _JSTR, window)
            match_format = _json_str(r'"matchFormat":' + _JSTR, window)
            team_names = [
                json.loads('"' + t + '"')
                for t in re.findall(r'"teamName":' + _JSTR, window)[:2]
            ]
            ground = _json_str(r'"ground":' + _JSTR, window)
            city = _json_str(r'"city":' + _JSTR, window)

            # startDate appears both quoted and unquoted (epoch milliseconds)
            m = re.search(r'"startDate":"?(\d{12,13})"?', window)
            event_date = self.to_iso_date(m.group(1)) if m else "TBD"

            if not series_name and not team_names:
                continue
            # Page includes live/recent matches; keep today onwards
            if event_date != "TBD" and event_date < today:
                continue

            seen_ids.add(match_id)

            name_parts = [p for p in [series_name, match_desc] if p]
            event_name = " - ".join(name_parts)
            if match_format:
                event_name = f"{event_name} ({match_format})" if event_name else match_format
            teams = " vs ".join(team_names)
            location = ", ".join(p for p in [ground, city] if p)

            events.append(self.normalize_event(
                sport="Cricket",
                event_name=event_name or teams,
                broadcaster="",
                event_date=event_date,
                location=location or "TBD",
                teams=teams
            ))

        logger.info(f"Found {len(events)} cricket events from Cricbuzz flight data")
        return events

    def _parse_dom_fallback(self, html):
        """Degraded fallback: match links from the server-rendered DOM (no dates)."""
        soup = BeautifulSoup(html, "html.parser")
        events = []
        seen = set()

        for link in soup.select('a[href^="/live-cricket-scores/"]'):
            title = link.get_text(strip=True)
            if len(title) < 10 or title in seen:
                continue
            seen.add(title)
            events.append(self.normalize_event(
                sport="Cricket",
                event_name=title,
                broadcaster="",
                event_date="TBD",
                location="TBD",
                teams=title
            ))
            if len(events) >= 30:
                break

        logger.info(f"Found {len(events)} cricket events from Cricbuzz DOM fallback")
        return events
