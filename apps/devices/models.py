from django.db import models
from django.db.models import Model
from utils.functional import unique_code


class Brand(Model):
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


class DeviceCategory(Model):
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


class Device(Model):
    """
    Device details table
    """

    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True)
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
        default="",
        verbose_name="Device version",
    )
    mpn = models.CharField(
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
    info = models.TextField(
        unique=False,
        null=False,
        blank=False,
        default="",
        verbose_name="Device description",
        help_text="format: required",
    )
    category = models.ForeignKey(DeviceCategory, on_delete=models.CASCADE)
    released = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Date Device released",
        help_text="format: Y-m-d H:M:S",
    )
    announced = models.DateTimeField(
        editable=False,
        auto_now=True,
        null=True,
        blank=True,
        verbose_name="Date Device announced",
        help_text="format: Y-m-d H:M:S",
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        related_name="children",
        null=True,
        blank=True,
        help_text="It can be used to form the table of content of the parent post of series.",
    )
    status = models.CharField(
        max_length=50,
        default="new inserted",
        choices=(
            ("new inserted", "New Inserted"),
            ("updated once", "Updated Once"),
            ("updated twice", "Updated twice"),
        ),
    )

    class Meta:
        unique_together = ("model", "mpn")

    @property
    def image(self):
        """Return an image url"""
        return self.media_set.filter(is_feature=True).first().image

    def source(self, src: str = "https://api.device-specs.io/api"):
        """Return the first device source object
        that match the src query
        """
        return self.devicesource_set.filter(source__icontains=src).first()

    def __str__(self):
        return f"{self.model} | {self.status}"

    def update_status(self):
        if self.status == "new inserted":
            self.status = "updated once"
        elif self.status == "updated once":
            self.status = "updated twice"
        self.save()
        return self


class DeviceSource(Model):
    """ """

    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    web_id = models.CharField(
        max_length=40,
        verbose_name="Device website ID",
    )
    source = models.CharField(
        max_length=40,
        verbose_name="Device source",
    )

    def __str__(self):
        return self.source


class Media(Model):
    """
    The Device image table.
    """

    device = models.ForeignKey(Device, on_delete=models.CASCADE)
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

    def __str__(self):
        return self.alt_text

    class Meta:
        verbose_name = "Device image"
        verbose_name_plural = "Device images"


class DeviceAttribute(Model):
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


class DeviceType(Model):
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


class DeviceTypeAttribute(Model):
    """
    Device type attributes link table
    """

    Device_attribute = models.ForeignKey(
        DeviceAttribute,
        related_name="Device_attribute",
        on_delete=models.PROTECT,
    )
    Device_type = models.ForeignKey(
        DeviceType,
        related_name="Device_type",
        on_delete=models.PROTECT,
    )

    class Meta:
        unique_together = ("Device_attribute", "Device_type")


class DeviceAttributeValue(Model):
    """
    Device attribute value table
    """

    Device_attribute = models.ForeignKey(
        DeviceAttribute,
        related_name="Device_attributes",
        on_delete=models.PROTECT,
    )
    attribute_value = models.CharField(
        max_length=255,
        unique=False,
        null=False,
        blank=False,
        verbose_name="attribute value",
    )


class DeviceAttributeValues(Model):
    """
    Device attribute values link table
    """

    attribute_values = models.ForeignKey(
        "DeviceAttributeValue",
        related_name="attribute_values",
        on_delete=models.PROTECT,
    )
    device = models.ForeignKey(Device, on_delete=models.CASCADE)

    class Meta:
        unique_together = (
            "attribute_values",
            "device",
        )
