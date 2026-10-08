import factory
from .models import Device, Telemetry, Alert
from django.utils import timezone

# Factory for Device model. Generates a unique device_code using a sequence.
class DeviceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Device

    name = factory.Faker("name")
    device_code = factory.Sequence(lambda n: f"inv-{n + 1:03d}")

# Factory for Telemetry model. Creates a related Device automatically.
class TelemetryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Telemetry

    device = factory.SubFactory(DeviceFactory)
    temperature = factory.Faker("random_int", min=25, max=70)
    power = factory.Faker("pyint", min_value=500, max_value=3000)
    voltage = factory.Faker("pyint", min_value=380, max_value=400)
    timestamp = factory.LazyFunction(timezone.now)