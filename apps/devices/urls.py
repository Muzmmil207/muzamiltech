from django.urls import path

from . import views

urlpatterns = [
    path("<str:brand>/<slug:model>", views.device_details, name="insert-devices"),
    path("<str:brand>", views.devices_by_brand, name="devices-by-brand"),
    path("insert", views.insert_devices_data, name="insert-devices"),
    path("update", views.update_devices_data, name="update-device"),
]
