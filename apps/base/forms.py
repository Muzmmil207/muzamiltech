from django import forms

from .models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["name", "email", "message"]
        widgets = {
            "message": forms.Textarea(attrs={"rows": 5}),
        }

    def clean_email(self):
        email = self.cleaned_data["email"]
        if "@example.com" in email:
            raise forms.ValidationError("We don't accept emails from example.com")
        return email

    def clean_name(self):
        name = self.cleaned_data["name"]
        if "@example.com" in name:
            raise forms.ValidationError("We don't accept names from example.com")
        return name
