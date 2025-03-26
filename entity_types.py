from datetime import datetime
from enum_types import FlightStatus
from dataclasses import dataclass, asdict
from typing import Optional, Dict


@dataclass
class Flight:
    flight_number: str
    departure_time: str
    arrival_time: str
    status: FlightStatus
    duration_minutes: Optional[int] = None

    def __init__(self, *args, **kwargs):
        # Handle dictionary input
        if len(args) == 1 and isinstance(args[0], dict) and not kwargs:
            kwargs = args[0]

        # Initialize dataclass fields
        self.flight_number = kwargs["flight_number"]
        self.departure_time = kwargs["departure_time"]
        self.arrival_time = kwargs["arrival_time"]
        self.status = kwargs["status"]
        self.duration_minutes = kwargs.get("duration_minutes")

        # Run validation
        self.__post_init__()

    def __post_init__(self):
        # Flight Status Validation
        FlightStatus.validate(self.status)

        # Duration Minutes Calculation
        if self.duration_minutes is None:
            self.duration_minutes = self._calculate_duration()

    def _calculate_duration(self) -> int:
        dep = datetime.strptime(self.departure_time, "%Y-%m-%d %H:%M")
        arr = datetime.strptime(self.arrival_time, "%Y-%m-%d %H:%M")

        if arr <= dep:
            raise ValueError("Arrival time must be after departure time")

        duration = int((arr - dep).total_seconds() / 60)
        if duration <= 0:
            raise ValueError("Duration must be positive")
        return duration

    def to_dict(self) -> Dict:
        return asdict(self)
