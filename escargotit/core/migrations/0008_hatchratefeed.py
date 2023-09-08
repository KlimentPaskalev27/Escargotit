# Generated by Django 4.2.2 on 2023-09-07 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_snailhatchrate_datetime_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='HatchRateFeed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('hatch_rate', models.DecimalField(decimal_places=2, max_digits=5)),
                ('grams_feed_given', models.IntegerField()),
            ],
        ),
    ]
