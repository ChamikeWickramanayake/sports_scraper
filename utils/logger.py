"""
Logging setup for Sports Events Scraper
"""
import logging
import sys
from config.config import LOG_FILE, LOG_LEVEL

def setup_logger(name="sports_scraper"):
    """Configure logger with file and console handlers"""
    logger = logging.getLogger(name)
    if logger.handlers:  # Already configured; don't duplicate handlers
        return logger

    level = getattr(logging, LOG_LEVEL, None)
    if not isinstance(level, int):
        level = logging.INFO
    logger.setLevel(level)
    logger.propagate = False

    # File handler (explicit UTF-8: the Windows default cp1252 can't encode
    # characters like → or ✓ and silently drops those log records)
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setLevel(level)

    # Console handler (make stdout tolerant of non-cp1252 characters on Windows)
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)

    # Formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

logger = setup_logger()
