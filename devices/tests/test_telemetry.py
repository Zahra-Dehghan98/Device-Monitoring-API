from rest_framework.test import APITestCase
from ..factories import DeviceFactory
from ..models import Telemetry

class TelemetryApiTestCase(APITestCase):
    # Tests for telemetry ingestion and input validation.
    def setUp(self):
        # Common setup: one device and a valid telemetry payload.
        self.device = DeviceFactory(device_code = "inv-001")
        self.data = {
            "device_code": "inv-001",
            "temperature": 50,
            "power" : 1000,
            "voltage" : 390,
            "timestamp" : "2026-10-07T10:00:00Z"
            }
        
    # Valid telemetry should be stored and return 201.
    def test_create_telemetry(self):
        response = self.client.post("/api/telemetry/", self.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Telemetry.objects.count(), 1)

    # Unknown device_code should return 404.
    def test_invalid_device_code(self):
        self.data["device_code"] = "invalid"
        response = self.client.post("/api/telemetry/", self.data)
        self.assertEqual(response.status_code, 404)

    # Missing required fields should return 400.
    def test_invalid_empty_field(self):
        data = {"device_code": self.device.device_code}
        response = self.client.post("/api/telemetry/", data)
        self.assertEqual(response.status_code, 400)

    # Non-numeric values for temperature, power, and voltage should return 400.
    def test_invalid_values(self):
        for field in ["temperature", "power", "voltage"]:
            with self.subTest(field=field):
                data = self.data.copy()
                data[field] = "invalid"
                response = self.client.post("/api/telemetry/", data)
                self.assertEqual(response.status_code, 400)

    # Malformed timestamp should return 400.
    def test_invalid_timestamp(self):
        self.data["timestamp"] = "not-date"
        response = self.client.post("/api/telemetry/", self.data)
        self.assertEqual(response.status_code, 400)

    # Negative power/voltage should return 400.
    def test_invalid_negative_values(self):
        for field in ["power", "voltage"]:
            with self.subTest(field=field):
                data = self.data.copy()
                data[field] = -100
                response = self.client.post("/api/telemetry/", data)
                self.assertEqual(response.status_code, 400)