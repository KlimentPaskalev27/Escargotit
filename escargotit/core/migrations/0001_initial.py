# Generated by Django 4.2.2 on 2023-09-06 15:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import picklefield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SnailBed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bed_name', models.CharField(blank=True, max_length=100, null=True)),
                ('snail_amount', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SnailFeed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('consumed_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('grams_feed_given', models.IntegerField()),
                ('snail_bed', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.snailbed')),
            ],
        ),
        migrations.CreateModel(
            name='SnailHatchRate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preexisting_snail_amount', models.IntegerField(blank=True, null=True)),
                ('newly_hatched_snails', models.IntegerField()),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('snail_bed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.snailbed')),
            ],
        ),
        migrations.CreateModel(
            name='SnailMortalityRate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preexisting_snail_amount', models.IntegerField(blank=True, null=True)),
                ('expired_snail_amount', models.IntegerField(default=0)),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('snail_bed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.snailbed')),
            ],
        ),
        migrations.CreateModel(
            name='TimeTakenToMature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('snail_hatched', models.DateTimeField(default=django.utils.timezone.now)),
                ('snail_matured', models.DateTimeField(default=django.utils.timezone.now)),
                ('snail_bed', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.snailbed')),
            ],
        ),
        migrations.CreateModel(
            name='SnailPerformance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('normalized_hatch_rate', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('normalized_mortality_rate', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('expected_time_to_maturity', models.PositiveIntegerField(blank=True, null=True)),
                ('snail_bed', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.snailbed')),
                ('snail_feed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.snailfeed')),
                ('snail_hatch_rate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.snailhatchrate')),
                ('snail_mortality_rate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.snailmortalityrate')),
                ('time_taken_to_mature', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.timetakentomature')),
            ],
        ),
        migrations.AddField(
            model_name='snailbed',
            name='hatch_rate',
            field=models.ForeignKey(blank=True, default=0, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.snailhatchrate'),
        ),
        migrations.AddField(
            model_name='snailbed',
            name='mortality_rate',
            field=models.ForeignKey(blank=True, default=0, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.snailmortalityrate'),
        ),
        migrations.AddField(
            model_name='snailbed',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='ForecastedHatchRate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('forecasted_value', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('forecasted_value_pyaf', picklefield.fields.PickledObjectField(editable=False)),
                ('snail_bed', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.snailbed')),
            ],
        ),
    ]
