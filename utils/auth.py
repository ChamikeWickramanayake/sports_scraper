"""
Google Sheets Authentication Module
"""
from google.oauth2.service_account import Credentials
from config.config import CREDENTIALS_FILE, SCOPES
from utils.logger import logger

def get_service_account_credentials():
    """
    Get Google service account credentials from JSON file.
    
    Note: Download credentials.json from Google Cloud Console:
    1. Create a service account
    2. Create a JSON key
    3. Place it in config/credentials.json
    
    Returns:
        Credentials: Google service account credentials
    """
    try:
        if not CREDENTIALS_FILE.exists():
            logger.error(
                f"Credentials file not found at {CREDENTIALS_FILE}\n"
                "Please download it from Google Cloud Console and place it there."
            )
            raise FileNotFoundError(f"Credentials file not found: {CREDENTIALS_FILE}")
        
        credentials = Credentials.from_service_account_file(
            CREDENTIALS_FILE, scopes=SCOPES
        )
        logger.info("Successfully loaded Google service account credentials")
        return credentials
    except Exception as e:
        logger.error(f"Failed to load credentials: {e}")
        raise
