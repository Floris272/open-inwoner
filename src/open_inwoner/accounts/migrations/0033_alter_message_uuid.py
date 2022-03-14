# Generated by Django 3.2.12 on 2022-03-14 10:57

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0032_gen_message_uuid"),
    ]

    operations = [
        migrations.AlterField(
            model_name="message",
            name="uuid",
            field=models.UUIDField(
                default=uuid.uuid4,
                help_text="Unique identifier",
                unique=True,
                verbose_name="UUID",
            ),
        ),
    ]
