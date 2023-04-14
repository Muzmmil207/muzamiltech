from django.db import models
from django.utils.translation import gettext_lazy as _


class AbstractModel(models.Model):
    """Abstract base model for create and update timestamp and author for all models."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
