from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _


class AbstractModel(models.Model):
    """Abstract base model for for all models."""

    slug = models.SlugField(
        max_length=150,
        null=False,
        unique=False,
        blank=False,
        verbose_name="Brand safe URL",
        help_text="format: required, letters, numbers, underscore, or hyphens",
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.slug)
        super().save(*args, **kwargs)

    class Meta:
        abstract = True
