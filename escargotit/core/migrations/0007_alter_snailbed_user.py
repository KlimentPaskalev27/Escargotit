# Generated by Django 4.2.2 on 2023-09-08 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_snailbed_hatch_rate_snailbed_mortality_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='snailbed',
            name='user',
            field=models.ManyToManyField(blank=True, db_constraint=False, null=True, to='core.profile'),
        ),
    ]
