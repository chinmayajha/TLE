# Generated by Django 4.0.2 on 2022-02-17 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playground', '0029_customer_score1_customer_score2'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='score3',
            field=models.IntegerField(default=0),
        ),
    ]
