from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from utils import validators


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

    name = models.CharField(max_length=255, validators=[validators.name_regex])
    email = models.EmailField(_("email address"), validators=[validators.email_regex])
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.email}): {self.message[:20]}"
