# Generated by Django 4.0.1 on 2022-01-27 17:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('playground', '0027_customer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='discord_handle',
            new_name='cf_handle',
        ),
    ]
