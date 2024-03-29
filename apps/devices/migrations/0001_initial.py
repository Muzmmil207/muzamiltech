# Generated by Django 4.1.7 on 2023-05-13 08:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("articles", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Brand",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        help_text="format: required, letters, numbers, underscore, or hyphens",
                        max_length=150,
                        verbose_name="Brand safe URL",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="format: required, unique, max-255",
                        max_length=15,
                        unique=True,
                        verbose_name="brand name",
                    ),
                ),
            ],
            options={
                "db_table": "brand",
            },
        ),
        migrations.CreateModel(
            name="Device",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        help_text="format: required, letters, numbers, underscore, or hyphens",
                        max_length=150,
                        verbose_name="Brand safe URL",
                    ),
                ),
                (
                    "model",
                    models.CharField(
                        db_index=True, max_length=50, verbose_name="Device name"
                    ),
                ),
                (
                    "version",
                    models.CharField(
                        default="", max_length=15, verbose_name="Device version"
                    ),
                ),
                (
                    "mpn",
                    models.CharField(
                        blank=True,
                        max_length=15,
                        null=True,
                        verbose_name="Device version",
                    ),
                ),
                (
                    "info",
                    models.TextField(
                        default="",
                        help_text="format: required",
                        verbose_name="Device description",
                    ),
                ),
                (
                    "released",
                    models.DateTimeField(
                        blank=True,
                        help_text="format: Y-m-d H:M:S",
                        null=True,
                        verbose_name="Date Device released",
                    ),
                ),
                (
                    "announced",
                    models.DateTimeField(
                        auto_now=True,
                        help_text="format: Y-m-d H:M:S",
                        null=True,
                        verbose_name="Date Device announced",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("new inserted", "New Inserted"),
                            ("updated once", "Updated Once"),
                            ("updated twice", "Updated twice"),
                        ],
                        default="new inserted",
                        max_length=50,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="DeviceAttribute",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "attribute",
                    models.CharField(
                        max_length=50, unique=True, verbose_name="attribute"
                    ),
                ),
            ],
            options={
                "db_table": "devices_attributes",
            },
        ),
        migrations.CreateModel(
            name="DeviceType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="format: required, unique, max-255",
                        max_length=255,
                        unique=True,
                        verbose_name="type of Device",
                    ),
                ),
            ],
            options={
                "db_table": "device_types",
            },
        ),
        migrations.CreateModel(
            name="Media",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    models.URLField(
                        default="images/default.png",
                        help_text="format: required, default-default.png",
                        verbose_name="Device image",
                    ),
                ),
                (
                    "alt_text",
                    models.CharField(max_length=255, verbose_name="alternative text"),
                ),
                (
                    "is_feature",
                    models.BooleanField(
                        default=False,
                        help_text="format: default=false, true=default image",
                        verbose_name="Device default image",
                    ),
                ),
                (
                    "device",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="devices.device"
                    ),
                ),
            ],
            options={
                "verbose_name": "Device image",
                "verbose_name_plural": "Device images",
                "db_table": "media",
            },
        ),
        migrations.CreateModel(
            name="DeviceTypeAttribute",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="format: required, unique, max-255",
                        max_length=255,
                        unique=True,
                        verbose_name="Device attribute name",
                    ),
                ),
                (
                    "device_type_attributes",
                    models.ManyToManyField(
                        related_name="device_type_attributes", to="devices.devicetype"
                    ),
                ),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        help_text="It can be used to form the table of content of the parent post of series.",
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="children",
                        to="devices.devicetypeattribute",
                    ),
                ),
            ],
            options={
                "db_table": "devices_types_attributes",
            },
        ),
        migrations.CreateModel(
            name="DeviceAttributeValue",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("value", models.CharField(max_length=255)),
                (
                    "device",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="devices",
                        to="devices.device",
                    ),
                ),
                (
                    "device_attribute",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="device_Attributes",
                        to="devices.deviceattribute",
                    ),
                ),
            ],
            options={
                "db_table": "devices_attributes_values",
            },
        ),
        migrations.AddField(
            model_name="deviceattribute",
            name="device_type_attribute",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="device_attributes",
                to="devices.devicetypeattribute",
            ),
        ),
        migrations.AddField(
            model_name="device",
            name="attributes",
            field=models.ManyToManyField(
                related_name="attributes",
                through="devices.DeviceAttributeValue",
                to="devices.deviceattribute",
            ),
        ),
        migrations.AddField(
            model_name="device",
            name="brand",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="devices.brand",
            ),
        ),
        migrations.AddField(
            model_name="device",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="articles.category"
            ),
        ),
        migrations.AddField(
            model_name="device",
            name="parent",
            field=models.ForeignKey(
                blank=True,
                help_text="It can be used to form the table of content of the parent post of series.",
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="children",
                to="devices.device",
            ),
        ),
        migrations.AddField(
            model_name="device",
            name="type",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="devices.devicetype",
            ),
        ),
        migrations.CreateModel(
            name="DeviceSource",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "web_id",
                    models.CharField(max_length=40, verbose_name="Device website ID"),
                ),
                (
                    "source",
                    models.CharField(max_length=40, verbose_name="Device source"),
                ),
                (
                    "device",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="device_Source",
                        to="devices.device",
                    ),
                ),
            ],
            options={
                "db_table": "devices_sources",
                "unique_together": {("web_id", "source")},
            },
        ),
        migrations.AlterUniqueTogether(
            name="device",
            unique_together={("model", "version")},
        ),
    ]
