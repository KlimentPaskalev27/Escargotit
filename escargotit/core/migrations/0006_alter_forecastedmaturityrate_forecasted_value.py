# Generated by Django 4.2.2 on 2023-09-14 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_snailbed_snail_feed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forecastedmaturityrate',
            name='forecasted_value',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=10, null=True),
        ),
    ]
