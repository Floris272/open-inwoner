# Generated by Django 4.2.11 on 2024-05-15 14:44

from django.db import migrations

import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ("configurations", "0066_merge_20240405_1100"),
    ]

    operations = [
        migrations.AlterField(
            model_name="siteconfiguration",
            name="warning_banner_text",
            field=ckeditor.fields.RichTextField(
                blank=True,
                help_text="Text will be displayed on the warning banner",
                verbose_name="Warning banner text",
            ),
        ),
    ]
