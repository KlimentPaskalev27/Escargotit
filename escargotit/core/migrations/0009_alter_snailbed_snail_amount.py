# Generated by Django 4.2.2 on 2023-09-06 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_snailmortalityrate_datetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='snailbed',
            name='snail_amount',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
