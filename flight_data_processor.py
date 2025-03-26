from typing import List

from enum_types import FlightStatus
from entity_types import Flight


class FlightDataProcessor:
    def __init__(self, data: list[dict]):
        self.flights: list[dict] = data.copy()
        self._validate_flights()

    def _validate_flights(self) -> None:
        for i, flight in enumerate(self.flights):
            self.flights[i] = self._validate_flight(flight)

    def _validate_flight(self, flight) -> dict:
        f = Flight(flight)
        return f.to_dict()

    def add_flight(self, data: dict) -> None:
        for i, f in enumerate(self.flights):
            if f["flight_number"] == data["flight_number"]:
                raise ValueError("flight already exist")
        data = self._validate_flight(data)
        self.flights.append(data)

    def remove_flight(self, flight_number: str) -> None:
        for i, f in enumerate(self.flights):
            if f["flight_number"] == flight_number:
                self.flights.pop(i)
                return None
        raise ValueError(f"No Flight Number Found {flight_number}")

    def flights_by_status(self, status: str) -> List[dict]:
        FlightStatus.validate(status)
        return [flight for flight in self.flights if flight["status"] == status]

    def get_longest_flight(self) -> dict:
        return max(self.flights, key=lambda x: x["duration_minutes"])

    def update_flight_status(
        self, flight_number: str, new_status: FlightStatus
    ) -> None:
        FlightStatus.validate(new_status)  # validate Flight status
        for flight in self.flights:
            if flight["flight_number"] == flight_number:
                flight["status"] = new_status
                return None
        raise ValueError(f"No Flight Number Found {flight_number}")
