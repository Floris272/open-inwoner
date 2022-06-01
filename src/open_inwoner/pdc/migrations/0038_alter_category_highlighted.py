# Generated by Django 3.2.13 on 2022-06-01 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdc', '0037_category_highlighted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='highlighted',
            field=models.BooleanField(default=False, help_text='Wether the category should be highlighted or not.', verbose_name='Highlighted'),
        ),
    ]
