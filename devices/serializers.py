from rest_framework import serializers
from .models import Device, Telemetry, Alert
from rest_framework.generics import get_object_or_404

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = "__all__"
        read_only_fields = ["id", "created_at"]

class TelemetrySerializer(serializers.ModelSerializer):
    device_code = serializers.CharField(max_length=50, write_only=True)

    class Meta:
        model = Telemetry
        fields = ["device_code", "temperature", "power", "voltage", "timestamp"]

    def create(self, validated_data):
        device_code = validated_data.pop("device_code")
        device = get_object_or_404(Device, device_code=device_code)
        validated_data["device"] = device
        instance = super().create(validated_data)
        if instance.temperature > 70:
            Alert.objects.create(
                device = instance.device,
                alert_type = Alert.ALERT_TYPE_CHOICES.HIGH_TEMPERATURE,
                recorded_value = instance.temperature,
            )
        return instance
        
class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = ["device", "alert_type", "recorded_value", "created_at", "is_resolved"]