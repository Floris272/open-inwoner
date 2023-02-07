# Generated by Django 3.2.15 on 2023-02-07 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("openzaak", "0011_auto_20230207_1030"),
    ]

    operations = [
        migrations.AddField(
            model_name="zaaktypeinformatieobjecttypeconfig",
            name="document_notification_enabled",
            field=models.BooleanField(
                default=False,
                help_text="When enabled the user will receive a notification when a visible document is added to the case",
                verbose_name="Enable document notification",
            ),
        ),
    ]
