# Generated by Django 4.0.1 on 2022-01-22 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playground', '0007_resources_alter_customer_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='resources',
            name='description',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='resources',
            name='link',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
