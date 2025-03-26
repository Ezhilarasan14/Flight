from enum import Enum


class FlightStatus(Enum):
    ON_TIME = "ON_TIME"
    DELAYED = "DELAYED"
    CANCELLED = "CANCELLED"

    @staticmethod
    def validate(status_str):
        try:
            return FlightStatus(status_str)
        except ValueError:
            raise ValueError(f"Flight status is not defined: {status_str}")
