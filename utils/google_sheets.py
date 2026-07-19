"""
Google Sheets API Wrapper
Handles all interactions with Google Sheets
"""
from googleapiclient.discovery import build
from datetime import datetime
from config.config import GOOGLE_SHEET_ID, SHEET_COLUMNS
from utils.auth import get_service_account_credentials
from utils.logger import logger

class GoogleSheetsAPI:
    def __init__(self):
        """Initialize Google Sheets API client"""
        self.credentials = get_service_account_credentials()
        self.service = build("sheets", "v4", credentials=self.credentials)
        self.sheet_id = GOOGLE_SHEET_ID
        
        if not self.sheet_id:
            logger.error("GOOGLE_SHEET_ID not configured. Set it in config.py or as environment variable.")
            raise ValueError("GOOGLE_SHEET_ID not configured")
    
    def append_row(self, values, range_name="Sheet1!A1"):
        """
        Append a row of data to the sheet.
        
        Args:
            values (list): Values to append
            range_name (str): Sheet range (e.g., "Sheet1!A1")
        """
        try:
            body = {"values": [values]}
            result = self.service.spreadsheets().values().append(
                spreadsheetId=self.sheet_id,
                range=range_name,
                valueInputOption="RAW",
                body=body,
            ).execute()
            logger.info(f"Appended row: {values[:3]}...")  # Log first 3 columns
            return result
        except Exception as e:
            logger.error(f"Failed to append row: {e}")
            raise
    
    def append_events(self, events, sheet_name="Sheet1"):
        """
        Append multiple events to the sheet, avoiding duplicates.
        
        Args:
            events (list): List of event dictionaries
            sheet_name (str): Name of the sheet
        """
        # Fetch existing data
        existing_data = self.get_all_rows(sheet_name)
        existing_events = set()
        
        for row in existing_data[1:]:  # Skip header
            if len(row) >= 5:
                event_key = (row[0], row[1], row[3], row[4])  # Sport, Event, Date, Location
                existing_events.add(event_key)
        
        # Filter out duplicates
        new_events = []
        for event in events:
            event_key = (
                event.get("sport", ""),
                event.get("event_name", ""),
                event.get("event_date", ""),
                event.get("location", ""),
            )
            if event_key not in existing_events:
                new_events.append(event)
                existing_events.add(event_key)
        
        # Append new events
        if not new_events:
            logger.info("No new events to append (all duplicates)")
            return
        
        for event in new_events:
            row = [
                event.get("sport", ""),
                event.get("event_name", ""),
                event.get("broadcaster", ""),
                event.get("event_date", ""),
                event.get("location", ""),
                event.get("teams", ""),
                event.get("source", ""),
                datetime.now().isoformat(),
            ]
            self.append_row(row, f"{sheet_name}!A1")
        
        logger.info(f"Appended {len(new_events)} new events to Google Sheets")
    
    def get_all_rows(self, sheet_name="Sheet1"):
        """
        Get all rows from the sheet.
        
        Args:
            sheet_name (str): Name of the sheet
            
        Returns:
            list: All rows from the sheet
        """
        try:
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.sheet_id,
                range=f"{sheet_name}!A:H",
            ).execute()
            rows = result.get("values", [])
            logger.debug(f"Retrieved {len(rows)} rows from sheet")
            return rows
        except Exception as e:
            logger.error(f"Failed to get rows: {e}")
            return []
    
    def clear_sheet(self, sheet_name="Sheet1"):
        """Clear all data from sheet (keeps header if present)"""
        try:
            self.service.spreadsheets().values().clear(
                spreadsheetId=self.sheet_id,
                range=f"{sheet_name}!A:H",
            ).execute()
            logger.info("Cleared sheet data")
        except Exception as e:
            logger.error(f"Failed to clear sheet: {e}")
    
    def create_header_row(self, sheet_name="Sheet1"):
        """Create header row if it doesn't exist"""
        try:
            header = [
                "Sport",
                "Event",
                "Broadcasting Partner",
                "Event Date",
                "Location",
                "Teams",
                "Source",
                "Last Updated",
            ]
            body = {"values": [header]}
            self.service.spreadsheets().values().update(
                spreadsheetId=self.sheet_id,
                range=f"{sheet_name}!A1:H1",
                valueInputOption="RAW",
                body=body,
            ).execute()
            logger.info("Created header row")
        except Exception as e:
            logger.error(f"Failed to create header: {e}")
