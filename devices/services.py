from rest_framework.exceptions import ValidationError
from .models import Device, Alert

def process_telemetry(serializer):
    device_code = serializer.validated_data["device_code"]
    device = Device.objects.filter(device_code=device_code).first()
    if not device:
        raise ValidationError(f"the device {device_code} is not exist")
    if not device.is_active:
        raise ValidationError(f"the device {device_code} is not activate")
    device_code = serializer.validated_data.pop("device_code")
    serializer.validated_data["device"] = device
    instance = serializer.save()
    if instance.temperature > 70:
        Alert.objects.create(
            device=instance.device,
            alert_type=Alert.ALERT_TYPE_CHOICES.HIGH_TEMPERATURE,
            recorded_value=instance.temperature
        )
    else:
        alert = Alert.objects.filter(device=device, is_resolved=False).first()
        if alert:
            alert.is_resolved = True
            alert.save()
    return instance