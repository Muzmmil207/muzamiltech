# Generated by Django 4.1.7 on 2023-05-01 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("devices", "0002_device_status_alter_devicesource_source"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="device",
            unique_together=set(),
        ),
        migrations.AddField(
            model_name="device",
            name="mpn",
            field=models.CharField(
                default="", max_length=15, verbose_name="Device version"
            ),
        ),
        migrations.AlterField(
            model_name="device",
            name="version",
            field=models.CharField(
                default="", max_length=15, verbose_name="Device version"
            ),
        ),
        migrations.AlterUniqueTogether(
            name="device",
            unique_together={("model", "mpn")},
        ),
    ]