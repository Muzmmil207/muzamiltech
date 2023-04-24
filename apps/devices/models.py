from django.db import models


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
        verbose_name = "Device category"
        verbose_name_plural = "Device categories"

    def __str_(self):
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
    slug = models.SlugField(
        max_length=255,
        unique=False,
        null=False,
        blank=False,
        verbose_name="Device safe URL",
        help_text="format: required, letters, numbers, underscores or hyphens",
    )
    model = models.CharField(
        max_length=50,
        unique=False,
        null=False,
        blank=False,
        verbose_name="Device name",
        help_text="format: required, max-255",
    )
    description = models.TextField(
        unique=False,
        null=False,
        blank=False,
        verbose_name="Device description",
        help_text="format: required",
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_active = models.BooleanField(
        unique=False,
        null=False,
        blank=False,
        default=True,
        verbose_name="Device visibility",
        help_text="format: true=Device visible",
    )
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

    def __str_(self):
        return self.model


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

    def __str_(self):
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

    def __str_(self):
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
        help_text="format: required, max-255",
    )


class DeviceInventory(models.Model):
    """
    Device inventory table
    """

    sku = models.CharField(
        max_length=20,
        unique=True,
        null=False,
        blank=False,
        verbose_name="stock keeping unit",
        help_text="format: required, unique, max-20",
    )
    upc = models.CharField(
        max_length=12,
        unique=True,
        null=False,
        blank=False,
        verbose_name="universal Device code",
        help_text="format: required, unique, max-12",
    )
    Device_type = models.ForeignKey(
        DeviceType, related_name="Device_type", on_delete=models.PROTECT
    )
    Device = models.ForeignKey(Device, related_name="Device", on_delete=models.PROTECT)
    brand = models.ForeignKey(Brand, related_name="brand", on_delete=models.PROTECT)
    attribute_values = models.ManyToManyField(
        DeviceAttributeValue,
        related_name="Device_attribute_values",
        through="DeviceAttributeValues",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Device visibility",
        help_text="format: true=Device visible",
    )
    is_default = models.BooleanField(
        default=False,
        verbose_name="default selection",
        help_text="format: true=sub Device selected",
    )
    retail_price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        unique=False,
        null=False,
        blank=False,
        verbose_name="recommended retail price",
        help_text="format: maximum price 999.99",
        error_messages={
            "name": {
                "max_length": "the price must be between 0 and 999.99.",
            },
        },
    )
    store_price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        unique=False,
        null=False,
        blank=False,
        verbose_name="regular store price",
        help_text="format: maximum price 999.99",
        error_messages={
            "name": {
                "max_length": "the price must be between 0 and 999.99.",
            },
        },
    )
    sale_price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        unique=False,
        null=False,
        blank=False,
        verbose_name="sale price",
        help_text="format: maximum price 999.99",
        error_messages={
            "name": {
                "max_length": "the price must be between 0 and 999.99.",
            },
        },
    )
    weight = models.FloatField(
        unique=False,
        null=False,
        blank=False,
        verbose_name="Device weight",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name="date sub-Device created",
        help_text="format: Y-m-d H:M:S",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="date sub-Device updated",
        help_text="format: Y-m-d H:M:S",
    )

    def __str_(self):
        return self.Device.name


class Media(models.Model):
    """
    The Device image table.
    """

    Device_inventory = models.ForeignKey(
        DeviceInventory,
        on_delete=models.PROTECT,
        related_name="media_Device_inventory",
    )
    image = models.ImageField(
        unique=False,
        null=False,
        blank=False,
        verbose_name="Device image",
        upload_to="images/",
        default="images/default.png",
        help_text="format: required, default-default.png",
    )
    alt_text = models.CharField(
        max_length=255,
        unique=False,
        null=False,
        blank=False,
        verbose_name="alternative text",
        help_text="format: required, max-255",
    )
    is_feature = models.BooleanField(
        default=False,
        verbose_name="Device default image",
        help_text="format: default=false, true=default image",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name="Device visibility",
        help_text="format: Y-m-d H:M:S",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="date sub-Device created",
        help_text="format: Y-m-d H:M:S",
    )

    class Meta:
        verbose_name = "Device image"
        verbose_name_plural = "Device images"


class Stock(models.Model):
    Device_inventory = models.OneToOneField(
        DeviceInventory,
        related_name="Device_inventory",
        on_delete=models.PROTECT,
    )
    last_checked = models.DateTimeField(
        unique=False,
        null=True,
        blank=True,
        verbose_name="inventory stock check date",
        help_text="format: Y-m-d H:M:S, null-true, blank-true",
    )
    units = models.IntegerField(
        default=0,
        unique=False,
        null=False,
        blank=False,
        verbose_name="units/qty of stock",
        help_text="format: required, default-0",
    )
    units_sold = models.IntegerField(
        default=0,
        unique=False,
        null=False,
        blank=False,
        verbose_name="units sold to date",
        help_text="format: required, default-0",
    )


class DeviceAttributeValues(models.Model):
    """
    Device attribute values link table
    """

    attributevalues = models.ForeignKey(
        "DeviceAttributeValue",
        related_name="attributevaluess",
        on_delete=models.PROTECT,
    )
    Deviceinventory = models.ForeignKey(
        DeviceInventory,
        related_name="Deviceattributevaluess",
        on_delete=models.PROTECT,
    )

    class Meta:
        unique_together = (
            "attributevalues",
            "Deviceinventory",
        )


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
        unique_together = (
            "Device_attribute",
            "Device_type",
        )
