# Generated by Django 4.2.2 on 2023-06-24 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_forecasted_forecasted_birth_rate_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ForecastedBirthRate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('forecasted_value', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
        migrations.DeleteModel(
            name='Forecasted',
        ),
    ]
