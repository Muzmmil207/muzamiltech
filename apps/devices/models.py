from apps.articles.models import Category
from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import Model
from utils.models.models_fields import AbstractModel


class CustomManager(BaseUserManager):
    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except ObjectDoesNotExist:
            return None


class Brand(AbstractModel):
    """
    Device brand table
    """

    class Meta:
        db_table = "brand"

    name = models.CharField(
        max_length=15,
        unique=True,
        null=False,
        blank=False,
        verbose_name="brand name",
        help_text="format: required, unique, max-255",
    )

    def __str__(self):
        return self.name


class Device(AbstractModel):
    """
    Device details table
    """

    class Meta:
        db_table = "device"

    objects = models.Manager()
    manager = CustomManager()

    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True)
    type = models.ForeignKey("DeviceType", on_delete=models.SET_NULL, null=True)
    model = models.CharField(
        max_length=50,
        unique=False,
        null=False,
        db_index=True,
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
    info = models.TextField(
        unique=False,
        null=False,
        blank=False,
        default="",
        verbose_name="Device description",
        help_text="format: required",
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
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
    attributes = models.ManyToManyField(
        "DeviceAttribute",
        related_name="attributes",
        through="DeviceAttributeValue",
    )

    class Meta:
        unique_together = ("model", "version")

    @property
    def image(self):
        """Return an image url"""
        return self.media_set.filter(is_feature=True).first().image

    @property
    def description(self):
        """A brief description"""
        os = self.devices.filter(device_attribute__attribute="os").first()
        if os:
            os = os.value
        diagonal = self.devices.filter(device_attribute__attribute="diagonal").first()
        if diagonal:
            diagonal = diagonal.value
        capacity = self.devices.filter(device_attribute__attribute="capacity").first()
        if capacity:
            capacity = capacity.value
        return f"{os or ''} - {diagonal or ''} - {capacity or ''}"

    def source(self, src: str = "https://api.device-specs.io/api"):
        """Return the first device source object
        that match the src query
        """
        return self.device_Source.filter(source__icontains=src).first()

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

    class Meta:
        unique_together = (
            "web_id",
            "source",
        )
        db_table = "devices_sources"

    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="device_Source")
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

    class Meta:
        verbose_name = "Device image"
        verbose_name_plural = "Device images"
        db_table = "media"

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


class DeviceType(Model):
    """
    Device type table
    """

    class Meta:
        db_table = "device_types"

    name = models.CharField(
        max_length=255,
        unique=True,
        null=False,
        blank=False,
        verbose_name="type of Device",
        help_text="format: required, unique, max-255",
    )

    def __str__(self):
        return self.name


class DeviceTypeAttribute(Model):
    """
    Device attribute table
    """

    class Meta:
        db_table = "devices_types_attributes"

    name = models.CharField(
        max_length=255,
        unique=True,
        null=False,
        blank=False,
        verbose_name="Device attribute name",
        help_text="format: required, unique, max-255",
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        related_name="children",
        null=True,
        blank=True,
        help_text="It can be used to form the table of content of the parent post of series.",
    )
    device_type_attributes = models.ManyToManyField(
        DeviceType,
        related_name="device_type_attributes",
    )

    def __str__(self):
        return self.name


class DeviceAttribute(Model):
    """
    Device attribute value table
    """

    class Meta:
        db_table = "devices_attributes"

    device_type_attribute = models.ForeignKey(
        DeviceTypeAttribute,
        related_name="device_attributes",
        on_delete=models.PROTECT,
    )
    attribute = models.CharField(
        max_length=50,
        unique=False,
        null=False,
        blank=False,
        verbose_name="attribute",
    )


class DeviceAttributeValue(Model):
    """
    Device attribute values link table
    """

    class Meta:
        db_table = "devices_attributes_values"

    device_attribute = models.ForeignKey(
        DeviceAttribute,
        related_name="device_Attributes",
        on_delete=models.PROTECT,
    )
    device = models.ForeignKey(Device, related_name="devices", on_delete=models.CASCADE)
    value = models.CharField(
        max_length=255,
        unique=False,
        null=False,
        blank=False,
    )
