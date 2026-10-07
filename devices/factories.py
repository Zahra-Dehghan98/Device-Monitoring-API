import factory
from .models import Device, Telemetry, Alert
from django.utils import timezone

class DeviceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Device

    name = factory.Faker("name")
    device_code = factory.Sequence(lambda n: f"inv-{n + 1:03d}")

class TelemetryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Telemetry

    device = factory.SubFactory(DeviceFactory)
    temperature = factory.Faker("random_int", min=25, max=70)
    power = factory.Faker("pyint", min=500, max=3000)
    voltage = factory.Faker("pyint", min=380, max=400)
    timestamp = factory.LazyFunction(timezone.now)