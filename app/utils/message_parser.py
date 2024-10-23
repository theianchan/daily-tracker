import re
from datetime import datetime, time
from app.models import HealthData


class MessageParser:
    @staticmethod
    def parse_message(message):
        message = message.lower().strip()

        # Check for summary request
        if message == "summary":
            return "SUMMARY_REQUEST"

        data = {}

        # Sleep time pattern: "sleep 1130pm"
        sleep_match = re.search(r"sleep\s+(\d{1,2})(\d{2})\s*([ap]m)", message)
        if sleep_match:
            hour, minute, meridiem = sleep_match.groups()
            hour = int(hour)
            if meridiem == "pm" and hour != 12:
                hour += 12
            elif meridiem == "am" and hour == 12:
                hour = 0
            data["sleep_time"] = time(hour=hour, minute=int(minute))

        # Wake time pattern: "wake 730am"
        wake_match = re.search(r"wake\s+(\d{1,2})(\d{2})\s*([ap]m)", message)
        if wake_match:
            hour, minute, meridiem = wake_match.groups()
            hour = int(hour)
            if meridiem == "pm" and hour != 12:
                hour += 12
            elif meridiem == "am" and hour == 12:
                hour = 0
            data["wake_time"] = time(hour=hour, minute=int(minute))

        # Blood pressure pattern: "bp 120/80"
        bp_match = re.search(r"bp\s+(\d{2,3})/(\d{2,3})", message)
        if bp_match:
            systolic, diastolic = bp_match.groups()
            data["blood_pressure_systolic"] = int(systolic)
            data["blood_pressure_diastolic"] = int(diastolic)

        # Phone usage pattern: "phone 45m"
        phone_match = re.search(r"phone\s+(\d+)m", message)
        if phone_match:
            minutes = phone_match.groups()[0]
            data["phone_minutes"] = int(minutes)

        data["date"] = datetime.now().date()
        return HealthData.from_dict(data)
