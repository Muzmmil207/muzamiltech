from django.contrib import admin

from .models import (
    Brand,
    Device,
    DeviceAttribute,
    DeviceAttributeValue,
    DeviceSource,
    DeviceType,
    DeviceTypeAttribute,
    Media,
)

admin.site.register(Brand)
admin.site.register(Device)
admin.site.register(Media)
admin.site.register(DeviceAttribute)
admin.site.register(DeviceAttributeValue)
admin.site.register(DeviceSource)
admin.site.register(DeviceType)
admin.site.register(DeviceTypeAttribute)
