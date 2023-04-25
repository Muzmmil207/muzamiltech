from django.db import models
from utils.functional import unique_code


class Category(models.Model):
    """
    Devices Categories table
    """

    name = models.CharField(
        max_length=100,
        null=False,
        unique=False,
        blank=False,
        verbose_name="category name",
        help_text="format: required, max-100",
    )
    slug = models.SlugField(
        max_length=150,
        null=False,
        unique=False,
        blank=False,
        verbose_name="category safe URL",
        help_text="format: required, letters, numbers, underscore, or hyphens",
    )

    class Meta:
        verbose_name = "Devices category"
        verbose_name_plural = "Devices categories"

    def __str__(self):
        return self.name


class Device(models.Model):
    """
    Device details table
    """

    web_id = models.CharField(
        max_length=40,
        default="",
        verbose_name="Device website ID",
    )
    model = models.CharField(
        max_length=50,
        unique=False,
        null=False,
        blank=False,
        verbose_name="Device name",
    )
    version = models.CharField(
        max_length=15,
        unique=False,
        null=True,
        blank=True,
        verbose_name="Device version",
    )
    slug = models.SlugField(
        max_length=255,
        unique=False,
        null=False,
        blank=False,
        verbose_name="Device safe URL",
        help_text="format: required, letters, numbers, underscores or hyphens",
    )
    description = models.TextField(
        unique=False,
        null=False,
        blank=False,
        default="",
        verbose_name="Device description",
        help_text="format: required",
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    released = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date Device released",
        help_text="format: Y-m-d H:M:S",
    )
    announced = models.DateTimeField(
        editable=False,
        auto_now=True,
        verbose_name="Date Device announced",
        help_text="format: Y-m-d H:M:S",
    )

    def __str__(self):
        return self.model

    class Meta:
        unique_together = ("model", "version")


class Brand(models.Model):
    """
    Device brand table
    """

    name = models.CharField(
        max_length=15,
        unique=True,
        null=False,
        blank=False,
        verbose_name="brand name",
        help_text="format: required, unique, max-255",
    )
    slug = models.SlugField(
        max_length=150,
        null=False,
        unique=False,
        blank=False,
        verbose_name="Brand safe URL",
        help_text="format: required, letters, numbers, underscore, or hyphens",
    )

    def __str__(self):
        return self.name


class DeviceAttribute(models.Model):
    """
    Device attribute table
    """

    name = models.CharField(
        max_length=255,
        unique=True,
        null=False,
        blank=False,
        verbose_name="Device attribute name",
        help_text="format: required, unique, max-255",
    )
    description = models.TextField(
        unique=False,
        null=False,
        blank=False,
        verbose_name="Device attribute description",
        help_text="format: required",
    )

    def __str__(self):
        return self.name


class DeviceType(models.Model):
    """
    Device type table
    """

    name = models.CharField(
        max_length=255,
        unique=True,
        null=False,
        blank=False,
        verbose_name="type of Device",
        help_text="format: required, unique, max-255",
    )

    Device_type_attributes = models.ManyToManyField(
        DeviceAttribute,
        related_name="Device_type_attributes",
        through="DeviceTypeAttribute",
    )

    def __str__(self):
        return self.name


class DeviceAttributeValue(models.Model):
    """
    Device attribute value table
    """

    Device_attribute = models.ForeignKey(
        DeviceAttribute,
        related_name="Device_attribute",
        on_delete=models.PROTECT,
    )
    attribute_value = models.CharField(
        max_length=255,
        unique=False,
        null=False,
        blank=False,
        verbose_name="attribute value",
    )


class Media(models.Model):
    """
    The Device image table.
    """

    image = models.URLField(
        unique=False,
        null=False,
        blank=False,
        verbose_name="Device image",
        default="images/default.png",
        help_text="format: required, default-default.png",
    )
    alt_text = models.CharField(
        max_length=255,
        unique=False,
        null=False,
        blank=False,
        verbose_name="alternative text",
    )
    is_feature = models.BooleanField(
        default=False,
        verbose_name="Device default image",
        help_text="format: default=false, true=default image",
    )

    class Meta:
        verbose_name = "Device image"
        verbose_name_plural = "Device images"


class DeviceAttributeValues(models.Model):
    """
    Device attribute values link table
    """

    attributevalues = models.ForeignKey(
        "DeviceAttributeValue",
        related_name="attributevaluess",
        on_delete=models.PROTECT,
    )

    # class Meta:
    #     unique_together = (
    #         "attributevalues",
    #         "Deviceinventory",
    #     )


class DeviceTypeAttribute(models.Model):
    """
    Device type attributes link table
    """

    Device_attribute = models.ForeignKey(
        DeviceAttribute,
        related_name="Deviceattribute",
        on_delete=models.PROTECT,
    )
    Device_type = models.ForeignKey(
        DeviceType,
        related_name="Devicetype",
        on_delete=models.PROTECT,
    )

    class Meta:
        unique_together = ("Device_attribute", "Device_type")
