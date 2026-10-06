from rest_framework import serializers
from .models import Device, Telemetry, Alert
from rest_framework.generics import get_object_or_404

# Serializer for Device model. Full CRUD support. 'id' and 'created_at' are read-only (auto-generated).
class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = "__all__"
        read_only_fields = ["id", "created_at"]

# Serializer for Telemetry model.


# and creates a high-temperature Alert if temperature > 70.
class TelemetrySerializer(serializers.ModelSerializer):
    # Expects 'device_code' (write-only) instead of 'device' id.
    device_code = serializers.CharField(max_length=50, write_only=True)
    class Meta:
        model = Telemetry
        fields = ["device_code", "temperature", "power", "voltage", "timestamp"]

    def create(self, validated_data):
        device_code = validated_data.pop("device_code")
        device = get_object_or_404(Device, device_code=device_code)
        # resolves device_code to a Device, saves the telemetry
        validated_data["device"] = device
        instance = super().create(validated_data)
        # creates a high-temperature Alert if temperature > 70.
        if instance.temperature > 70:
            Alert.objects.create(
                device=instance.device,
                alert_type=Alert.ALERT_TYPE_CHOICES.HIGH_TEMPERATURE,
                recorded_value=instance.temperature,
            )
        return instance

# Read-only serializer for the /devices/{id}/latest/ endpoint.
# Combines fields from both Telemetry and Device (device_code).
class DeviceLatestSerializer(serializers.Serializer):
    device = serializers.CharField(source = "device.device_code")
    temperature = serializers.DecimalField(max_digits=4, decimal_places=2)
    power = serializers.IntegerField()
    voltage = serializers.IntegerField()
    timestamp = serializers.DateTimeField()

# Read-only serializer for Alert model.
# Alerts are created automatically by the server, not by clients.        
class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = ["device", "alert_type", "recorded_value", "created_at", "is_resolved"]