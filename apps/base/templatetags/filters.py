from django import template

register = template.Library()
from apps.devices.models import Device, DeviceAttributeValue
from django.core.exceptions import ObjectDoesNotExist


@register.filter(name="replace")
def string_filter(value, arg):
    return value.replace(arg, " ")


@register.filter(name="value_filter")
def device_attribute_value_filter(queryset, device: Device):
    try:
        return DeviceAttributeValue.objects.get(device_attribute=queryset, device=device).value
    except ObjectDoesNotExist:
        return ""
