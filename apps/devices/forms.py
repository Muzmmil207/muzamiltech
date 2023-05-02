from django import forms

from .models import Device


class DeviceForm(forms.ModelForm):
    # status = forms.ModelChoiceField(empty_label="--Choose a status--")

    class Meta:
        model = Device
        fields = (
            "status",
            "category",
        )
