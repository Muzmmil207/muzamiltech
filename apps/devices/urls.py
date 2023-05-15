from django.urls import path

from . import views

urlpatterns = [
    path("", views.devices, name="devices"),
    path("devices-brands", views.brands, name="brands"),
    path("search", views.search_devices, name="search-devices"),
    path("insert", views.insert_devices_data, name="insert-devices"),
    path("update", views.update_devices_data, name="update-device"),
    path("<str:brand>/<slug:model>", views.device_details, name="device-details"),
    path("<str:brand>", views.devices_by_brand, name="devices-by-brand"),
]
