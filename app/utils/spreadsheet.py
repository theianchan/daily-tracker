import gspread
from oauth2client.service_account import ServiceAccountCredentials
from app.config import Config
from datetime import datetime, timedelta
import pandas as pd
import numpy as np


class SpreadsheetManager:
    def __init__(self):
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
        ]
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            Config.GOOGLE_CREDENTIALS_JSON, scope
        )
        self.client = gspread.authorize(credentials)
        self.sheet = self.client.open_by_key(Config.SPREADSHEET_ID).sheet1

    def append_row(self, data):
        return self.sheet.append_row(data)

    def get_date_data(self, date):
        date_str = date.strftime("%Y-%m-%d")
        cells = self.sheet.findall(date_str)
        if cells:
            row = self.sheet.row_values(cells[0].row)
            return row
        return None

    def get_7day_summary(self):
        # Get all data from last 7 days
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=7)

        # Get all rows
        all_data = self.sheet.get_all_records()

        # Convert to DataFrame
        df = pd.DataFrame(all_data)
        df["date"] = pd.to_datetime(df["date"])

        # Filter last 7 days
        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        recent_data = df.loc[mask]

        if recent_data.empty:
            return "No data available for the last 7 days."

        summary = []

        # Sleep duration
        recent_data["sleep_duration"] = (
            pd.to_datetime(recent_data["wake_time"])
            - pd.to_datetime(recent_data["sleep_time"])
        ).dt.total_seconds() / 3600
        avg_sleep = recent_data["sleep_duration"].mean()
        summary.append(f"Avg sleep: {avg_sleep:.1f}h")

        # Blood pressure
        avg_systolic = recent_data["blood_pressure_systolic"].mean()
        avg_diastolic = recent_data["blood_pressure_diastolic"].mean()
        summary.append(f"Avg BP: {avg_systolic:.0f}/{avg_diastolic:.0f}")

        # Phone usage
        avg_phone = recent_data["phone_minutes"].mean()
        summary.append(f"Avg phone use: {avg_phone:.0f}m")

        # Trends
        phone_trend = (
            recent_data["phone_minutes"].iloc[-1] - recent_data["phone_minutes"].iloc[0]
        )
        trend_indicator = "↑" if phone_trend > 0 else "↓" if phone_trend < 0 else "→"
        summary.append(f"Phone usage trend: {trend_indicator}")

        return "\n".join(summary)
