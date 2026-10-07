from rest_framework.test import APITestCase
from ..factories import DeviceFactory, TelemetryFactory
from ..models import Device

class DeviceApiTestCase(APITestCase):

    def test_create_device(self):
        # Creating a device via API should return 201 and persist one record.
        data = {"name": "inverter-1", "device_code": "inv-001"}
        response = self.client.post("/api/devices/", data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Device.objects.count(), 1)

    def test_devices_list(self):
         # Listing devices should return 200 with all devices (paginated).
        DeviceFactory.create_batch(10)
        response = self.client.get("/api/devices/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Device.objects.count(), 10)

    def test_device_retrieve(self):
        # Retrieving a single device by id should return 200.
        device = DeviceFactory()
        response = self.client.get(f"/api/devices/{device.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Device.objects.count(), 1)
  
    def test_device_partial_update(self):
        # PATCH should update only the provided fields
        device = DeviceFactory()
        response = self.client.patch(f"/api/devices/{device.id}/", {"name": "sample-name"})
        self.assertEqual(response.status_code, 200)
        device.refresh_from_db()
        self.assertEqual(device.name, "sample-name")

    def test_device_update(self):
        # PUT should replace all fields.
        device = DeviceFactory()
        response = self.client.put(f"/api/devices/{device.id}/", {"name": "sample-name", "device_code": "sample-code-1"})
        self.assertEqual(response.status_code, 200)
        device.refresh_from_db()
        self.assertEqual(device.name, "sample-name") 
        self.assertEqual(device.device_code, "sample-code-1")

    def test_device_delete(self):
        # DELETE should remove the device and return 204.
        device = DeviceFactory()
        response = self.client.delete(f"/api/devices/{device.id}/")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Device.objects.count(), 0)

    def test_device_validate_not_repeat(self):
        # device_code must be unique; duplicates should return 400.
        device = DeviceFactory()
        device.device_code = "inv-005"
        device.save()
        response = self.client.post(f"/api/devices/", {"name": "inverter-5", "device_code": "inv-005"})
        self.assertEqual(response.status_code, 400)

    def test_device_validate_no_empty(self):
        # Missing required fields should return 400.
        response = self.client.post(f"/api/devices/", {})
        self.assertEqual(response.status_code, 400)