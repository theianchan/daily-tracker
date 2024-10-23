import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
    TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER")
    SPREADSHEET_ID = os.environ.get("SPREADSHEET_ID")
    GOOGLE_CREDENTIALS_JSON = os.environ.get("GOOGLE_CREDENTIALS_JSON")
    TIMEZONE = "America/New_York"  # Adjust to your timezone

    # Reminder window (24-hour format)
    REMINDER_START_HOUR = 7  # 7 AM
    REMINDER_END_HOUR = 12  # 12 PM
    REMINDER_INTERVAL = 30  # Check every 30 minutes
