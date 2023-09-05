# Generated by Django 4.2.2 on 2023-09-05 13:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_snailbed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='snailbed',
            name='bed_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='snailbed',
            name='forecasted_birth_rate',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.forecastedbirthrate'),
        ),
        migrations.AlterField(
            model_name='snailbed',
            name='snail_birth_rate',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.snailbirthrate'),
        ),
        migrations.AlterField(
            model_name='snailbed',
            name='snail_feed',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.snailfeed'),
        ),
        migrations.AlterField(
            model_name='snailbed',
            name='snail_mortality_rate',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.snailmortalityrate'),
        ),
        migrations.AlterField(
            model_name='snailbed',
            name='snail_performance',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.snailperformance'),
        ),
        migrations.AlterField(
            model_name='snailbed',
            name='time_taken_to_mature',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.timetakentomature'),
        ),
    ]