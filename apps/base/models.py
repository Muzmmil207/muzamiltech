from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class NewsletterSubscriber(models.Model):
    class Meta:
        db_table = "news_letter_subscribers"

    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class Contact(models.Model):
    class Meta:
        db_table = "contacts"

    name = models.CharField(max_length=255)
    email_regex = RegexValidator(
        regex=r"^[A-z0-9\.]+@[A-z0-9]+\.(com|net|org|info)$",
        message=_("Email must be entered in the format: `abc@abc.com`."),
    )
    email = models.EmailField(_("email address"), validators=[email_regex])
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.email}): {self.message[:20]}"
