from django.db import models

# A device that sends monitoring data (temperature, power, voltage)
class Device(models.Model):
    name = models.CharField(max_length=100)
    device_code = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.device_code}"

# Readings (temperature, power, voltage) sent by a device at a specific time
class Telemetry(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="telemetries")
    temperature = models.DecimalField(max_digits=4, decimal_places=2)
    power = models.PositiveIntegerField()
    voltage = models.PositiveIntegerField()
    timestamp = models.DateTimeField(db_index=True)

    def __str__(self):
        return f"{self.device} - {self.temperature}"

# Created automatically when a device's temperature exceeds the allowed limit
class Alert(models.Model):
    class ALERT_TYPE_CHOICES(models.TextChoices):
        HIGH_TEMPERATURE = "high_temperature", "High_Temperature"
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="alerts")
    alert_type = models.CharField(choices=ALERT_TYPE_CHOICES.choices, max_length=50)
    recorded_value = models.DecimalField(max_digits=4, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.device} - {self.alert_type} - {self.is_resolved}"