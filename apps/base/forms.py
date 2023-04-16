from django import forms

from .models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["name", "email", "message"]
        widgets = {
            "message": forms.Textarea(attrs={"rows": 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update({"placeholder": "Your name"})
        self.fields["email"].widget.attrs.update({"placeholder": "Your email address"})
        self.fields["message"].widget.attrs.update({"placeholder": "Message"})

    def clean_email(self):
        email = self.cleaned_data["email"]
        if "@example.com" in email:
            raise forms.ValidationError("We don't accept emails from example.com")
        return email
