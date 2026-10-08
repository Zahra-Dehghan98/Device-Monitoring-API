from rest_framework.test import APITestCase
from ..factories import DeviceFactory, TelemetryFactory
from ..models import Alert, Telemetry

class AlertApiTestCase(APITestCase):
    def setUp(self):
        self.device = DeviceFactory(device_code = "inv-001")
        self.data = {
            "device_code": "inv-001",
            "temperature": 50,
            "power" : 1000,
            "voltage" : 390,
            "timestamp" : "2026-10-07T10:00:00Z"
        }

    def test_create_alert_gt_70(self):
        self.data["temperature"] = 75
        response = self.client.post("/api/telemetry/", self.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Telemetry.objects.count(), 1)
        self.assertEqual(Alert.objects.count(), 1)

    def test_not_create_alert_equal_70(self):
        self.data["temperature"] = 70
        response = self.client.post("/api/telemetry/", self.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Telemetry.objects.count(), 1)
        self.assertEqual(Alert.objects.count(), 0)

    def test_not_create_alert_lt_70(self):
        self.data["temperature"] = 69
        response = self.client.post("/api/telemetry/", self.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Telemetry.objects.count(), 1)
        self.assertEqual(Alert.objects.count(), 0)

    def test_resolve_alert(self):
        self.data["temperature"] = 75
        self.client.post("/api/telemetry/", self.data)
        self.assertFalse(Alert.objects.first().is_resolved)

        self.data["temperature"] = 42
        self.client.post("/api/telemetry/", self.data)
        self.assertTrue(Alert.objects.first().is_resolved)

    def test_alert_list(self):
        for _ in range(10):
            self.data["temperature"] = 75
            self.client.post("/api/telemetry/", self.data)
        response = self.client.get("/api/alerts/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Alert.objects.count(), 10)

    def test_alert_post_not_allowed(self):
        data = {}
        response = self.client.post("/api/alerts/", data)
        self.assertEqual(response.status_code, 405)

    def test_alert_delete_not_allowed(self):
        self.data["temperature"] = 75
        self.client.post("/api/telemetry/", self.data)
        alert_id = Alert.objects.first().id
        response = self.client.delete(f"/api/alerts/{alert_id}/")
        self.assertEqual(response.status_code, 405)
                           



