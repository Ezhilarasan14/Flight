import unittest

# from datetime import datetime
from flight_data_processor import FlightDataProcessor


class TestStringMethods(unittest.TestCase):
    def setUp(self):
        flight_data = [
            {
                "flight_number": "AZ001",
                "departure_time": "2025-02-19 15:30",
                "arrival_time": "2025-02-20 03:45",
                "status": "ON_TIME",
            },
            {
                "flight_number": "AZ002",
                "departure_time": "2025-02-21 11:00",
                "arrival_time": "2025-02-21 16:00",
                "status": "DELAYED",
            },
        ]
        self.obj = FlightDataProcessor(flight_data)

    def test_validate(self):
        self.assertEqual(type(self.obj), FlightDataProcessor)
        self.assertEqual(len(self.obj.flights), 2)

    def test_add_flight(self):
        new_data = {
            "flight_number": "AZ003",
            "departure_time": "2025-02-19 15:30",
            "arrival_time": "2025-02-20 02:40",
            "status": "ON_TIME",
        }
        self.obj.add_flight(new_data)
        # print("after add_flight :: ", self.obj.flights)
        self.assertEqual(len(self.obj.flights), 3)

        # Test duplicate flight
        with self.assertRaises(ValueError):
            self.obj.add_flight(new_data)

        # Test datetime format validation
        dup_data = new_data.copy()
        dup_data["flight_number"] = "AZ004"
        dup_data["departure_time"] = "abcd-ef-gh"

        with self.assertRaises(ValueError):
            self.obj.add_flight(dup_data)

    def test_remove_flight(self):
        self.obj.remove_flight("AZ001")
        # print("after remove_flight :: ", self.obj.flights)
        self.assertEqual(len(self.obj.flights), 1)

        # Test removing non-existent flight
        with self.assertRaises(ValueError):
            self.obj.remove_flight("ABCCBC")

    def test_flights_by_status(self):
        self.test_add_flight()
        on_time = self.obj.flights_by_status("ON_TIME")
        # print("on_time status :: ", on_time)
        self.assertEqual(len(on_time), 2)

        # Test invalid status
        with self.assertRaises(ValueError):
            self.obj.flights_by_status("SBSDFSD")

    def test_get_longest_flight(self):
        longest = self.obj.get_longest_flight()
        # print("longest flight :: ", longest)
        self.assertEqual(longest["flight_number"], "AZ001")
        self.assertEqual(longest["duration_minutes"], 735)

    def test_update_flight_status(self):
        self.obj.update_flight_status("AZ001", "CANCELLED")
        cancalled = self.obj.flights_by_status("CANCELLED")
        # print("after cancalled : ", cancalled)
        self.assertEqual(cancalled[0]["flight_number"], "AZ001")
        self.assertEqual(len(cancalled), 1)

        # Test invalid status
        with self.assertRaises(ValueError):
            self.obj.update_flight_status(flight_number="AZ001", new_status="adasdf")

        # Test non-existent flight
        with self.assertRaises(ValueError):
            self.obj.update_flight_status("ABCCAS", "ON_TIME")


if __name__ == "__main__":
    unittest.main()
