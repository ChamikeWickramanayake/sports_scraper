"""
Generic Scraper
Fallback scraper for sources without a dedicated implementation.

This is a low-precision heuristic: it surfaces plausible event/fixture links
from server-rendered pages. Dates are often "TBD" and news-heavy homepages
mostly yield headlines — results should be treated as leads, not fixtures.
"""
import re
from datetime import datetime, timedelta
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from scrapers.base_scraper import BaseScraper
from utils.logger import logger

_NAV_NOISE = re.compile(
    r"log\s?in|sign\s?up|subscribe|privacy|cookie|terms|about\s?us|contact|shop|"
    r"tickets?|newsletter|download|app\s?store|google\s?play|advertis|careers|faq",
    re.I,
)
_TEAMS = re.compile(r"\s+(?:vs?\.?|v)\s+", re.I)
_EVENT_KEYWORDS = re.compile(
    r"fixture|schedule|match|game|series|tournament|championship|cup|final|"
    r"open|grand.?prix|derby|qualifier|playoff|semi.?final",
    re.I,
)
_SPORT_KEYWORDS = {
    "Cricket": re.compile(r"cricket|t20|odi|\btest\b|ipl|\bbbl\b", re.I),
    "Football": re.compile(r"football|soccer|uefa|fifa|premier\s?league|la\s?liga", re.I),
    "Basketball": re.compile(r"basketball|\bnba\b|\bwnba\b|euroleague", re.I),
    "Tennis": re.compile(r"tennis|\batp\b|\bwta\b|slam|masters", re.I),
    "Rugby": re.compile(r"rugby|six\s?nations", re.I),
    "Baseball": re.compile(r"baseball|\bmlb\b|world\s?series", re.I),
    "American Football": re.compile(r"\bnfl\b|american\s?football|super\s?bowl", re.I),
    "Hockey": re.compile(r"hockey|\bnhl\b", re.I),
    "Golf": re.compile(r"golf|\bpga\b|ryder", re.I),
}
_MONTHS = (
    "jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec"
)
_DATE_ISO = re.compile(r"\b(\d{4}-\d{2}-\d{2})\b")
_DATE_DMY = re.compile(r"\b(\d{1,2})/(\d{1,2})/(\d{4})\b")
_DATE_MONTH = re.compile(
    r"\b(" + _MONTHS + r")[a-z]*\.?\s+(\d{1,2})(?:st|nd|rd|th)?(?:,?\s+(\d{4}))?\b",
    re.I,
)
MAX_EVENTS = 40

class GenericScraper(BaseScraper):
    """Generic scraper for sources without specific implementation"""

    def __init__(self, source_id, source_url, sports):
        super().__init__(source_id, source_url, sports)

    def _scrape(self):
        """
        Heuristic scraping: scan all anchors, keep only those with a positive
        event signal (teams pattern, event keyword, or parseable date).
        """
        logger.info(f"Scraping {self.source_id} (generic heuristic mode — low-confidence results)...")

        response = self.fetch_page(self.source_url)
        if not response:
            return []

        soup = BeautifulSoup(response.content, "html.parser")
        anchors = soup.find_all("a")

        events = []
        seen_hrefs = set()
        seen_texts = set()

        for link in anchors:
            try:
                text = link.get_text(" ", strip=True)
                href = link.get("href", "")
                if not text or not href:
                    continue

                # Size/shape filters
                if len(text) < 15 or len(text) > 120 or len(text.split()) < 3:
                    continue
                if _NAV_NOISE.search(text) or _NAV_NOISE.search(href):
                    continue

                # Positive signal required
                has_teams = bool(_TEAMS.search(text))
                event_date = self._extract_date(text, link)
                has_keyword = bool(_EVENT_KEYWORDS.search(text) or _EVENT_KEYWORDS.search(href))
                if not (has_teams or has_keyword or event_date):
                    continue

                # Dedupe by resolved href and normalized text
                abs_href = urljoin(self.source_url, href)
                norm_text = " ".join(text.lower().split())
                if abs_href in seen_hrefs or norm_text in seen_texts:
                    continue
                seen_hrefs.add(abs_href)
                seen_texts.add(norm_text)

                teams = ""
                if has_teams:
                    parts = [p.strip() for p in _TEAMS.split(text) if p.strip()]
                    if len(parts) >= 2:
                        teams = f"{parts[0]} vs {parts[1]}"

                events.append(self.normalize_event(
                    sport=self._detect_sport(text, href),
                    event_name=text[:100],
                    broadcaster=self.source_id,
                    event_date=event_date or "TBD",
                    location="TBD",
                    teams=teams
                ))
                if len(events) >= MAX_EVENTS:
                    break
            except Exception as e:
                logger.debug(f"Error parsing link: {e}")
                continue

        if not events:
            logger.warning(
                f"{self.source_id}: parsed {len(anchors)} anchors, 0 passed the event filters "
                "(page may be client-rendered or carry no fixture links)"
            )
        else:
            logger.info(f"Found {len(events)} potential events from {self.source_id} (heuristic)")
        return events

    def _detect_sport(self, text, href):
        """Match the anchor against this source's sports list by keyword."""
        haystack = f"{text} {href}"
        for sport in self.sports:
            pattern = _SPORT_KEYWORDS.get(sport)
            if pattern and pattern.search(haystack):
                return sport
        if len(self.sports) == 1:
            return self.sports[0]
        return "Sports"

    def _extract_date(self, text, link):
        """Try to pull an ISO date out of the anchor or its parent's text."""
        contexts = [text]
        if link.parent is not None:
            contexts.append(link.parent.get_text(" ", strip=True)[:300])

        for context in contexts:
            m = _DATE_ISO.search(context)
            if m:
                return self.to_iso_date(m.group(1))

            m = _DATE_DMY.search(context)
            if m:
                day, month, year = int(m.group(1)), int(m.group(2)), int(m.group(3))
                try:
                    return datetime(year, month, day).strftime("%Y-%m-%d")
                except ValueError:
                    continue

            m = _DATE_MONTH.search(context)
            if m:
                try:
                    month = datetime.strptime(m.group(1)[:3], "%b").month
                    day = int(m.group(2))
                    year = int(m.group(3)) if m.group(3) else datetime.now().year
                    parsed = datetime(year, month, day)
                    # No year given and date already passed: assume next year
                    if not m.group(3) and parsed < datetime.now() - timedelta(days=1):
                        parsed = datetime(year + 1, month, day)
                    return parsed.strftime("%Y-%m-%d")
                except ValueError:
                    continue
        return ""
