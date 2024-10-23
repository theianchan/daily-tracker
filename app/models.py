from dataclasses import dataclass
from datetime import datetime, time


@dataclass
class HealthData:
    date: datetime
    sleep_time: time = None
    wake_time: time = None
    blood_pressure_systolic: int = None
    blood_pressure_diastolic: int = None
    phone_minutes: int = None

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    def to_row(self):
        return [
            self.date.strftime("%Y-%m-%d"),
            self.sleep_time.strftime("%H:%M") if self.sleep_time else "",
            self.wake_time.strftime("%H:%M") if self.wake_time else "",
            str(self.blood_pressure_systolic) if self.blood_pressure_systolic else "",
            str(self.blood_pressure_diastolic) if self.blood_pressure_diastolic else "",
            str(self.phone_minutes) if self.phone_minutes else "",
        ]
