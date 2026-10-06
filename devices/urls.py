from rest_framework.routers import DefaultRouter
from .views import DeviceViewSet, TelemetryViewSet, AlertViewSet
from django.urls import path, include

router = DefaultRouter()

router.register(r"devices", DeviceViewSet, basename="device")
router.register(r"telemetry", TelemetryViewSet, basename="telemetry")
router.register(r"alerts", AlertViewSet, basename="alert")

urlpatterns = [
    path("api/", include(router.urls)),
]