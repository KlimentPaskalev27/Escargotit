import numpy as np
import pandas as pd
from django.db import models
from django.db.models import Max # used to compare datetimes
from django.db.models.signals import post_save # used to update a SnailBed property to point to new object
from django.dispatch import receiver # used to update a SnailBed property to point to new object
from neuralprophet import NeuralProphet # used to forecast data based on previous
from picklefield.fields import PickledObjectField # pickle together objects and data to be passed in
from django.contrib.auth.models import User # django User class ready to use
from django.utils import timezone


class SnailBed(models.Model):
    bed_name = models.CharField(max_length=100, unique=False, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    snail_amount = models.IntegerField(null=True, blank=True)
    mortality_rate = models.ForeignKey('SnailMortalityRate', on_delete=models.SET_NULL, null=True, blank=True, default=0)

    @property
    def mortality_percentage_rate(self):
        if self.mortality_rate:
            return self.mortality_rate
        return None

    def __str__(self):
        return self.bed_name

    def save(self, *args, **kwargs):
        # if user does not give name, give number defaults with counter
        if not self.bed_name:
            # Generate a default name with a counter
            existing_beds_with_default_name = SnailBed.objects.filter(bed_name__startswith='Snail Bed #').count()
            counter = existing_beds_with_default_name + 1
            self.bed_name = f'Snail Bed #{counter}'
        
        # If this is a new instance, initialize related properties to 0
        if self.snail_amount is None:
            self.snail_amount = 0

        super().save(*args, **kwargs)



class SnailFeed(models.Model):
    snail_bed = models.OneToOneField(SnailBed, on_delete=models.CASCADE)
    consumed_on = models.DateTimeField(default=timezone.now)
    grams_feed_given = models.IntegerField()

    def __int__(self):
        status = self.grams_feed_given
        return status

    def __str__(self):
        status = str(self.grams_feed_given) + " grams"
        return status

class SnailHatchRate(models.Model):
    snail_bed = models.OneToOneField(SnailBed, on_delete=models.CASCADE)
    hatch_date = models.DateField(default=timezone.now)
    preexisting_snail_amount = models.IntegerField(null=True, blank=True)
    newly_hatched_snails = models.IntegerField()
    hatch_rate_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk and self.snail_bed:
            self.preexisting_snail_amount = self.snail_bed.snail_amount

        if self.preexisting_snail_amount is not None and self.newly_hatched_snails is not None:
            self.snail_bed.snail_amount = self.preexisting_snail_amount + self.newly_hatched_snails
            self.snail_bed.save()

        if self.preexisting_snail_amount and self.newly_hatched_snails:
           self.hatch_rate_percentage = (self.newly_hatched_snails / self.preexisting_snail_amount) * 100

        super().save(*args, **kwargs)

    @property
    def hatch_rate_percentage(self):
        # Calculate hatch rate percentage based on other fields
        # Adjust the formula according to your specific calculation
        if self.preexisting_snail_amount > 0:
            return (self.newly_hatched_snails / self.preexisting_snail_amount) * 100
        else:
            return 0

    def __int__(self):
        return int(self.hatch_rate_percentage)

    def __str__(self):
        status = str(self.hatch_rate_percentage) + "%"
        return status


class SnailMortalityRate(models.Model):
    snail_bed = models.ForeignKey(SnailBed, on_delete=models.CASCADE)
    preexisting_snail_amount = models.IntegerField(null=True, blank=True)
    expired_snail_amount = models.IntegerField(default=0)
    mortality_rate_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    datetime = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.preexisting_snail_amount = self.snail_bed.snail_amount

        if self.preexisting_snail_amount and self.expired_snail_amount:
            self.snail_bed.snail_amount = self.preexisting_snail_amount - self.expired_snail_amount
            self.snail_bed.save()

        super().save(*args, **kwargs)

    @property
    def mortality_rate_percentage(self):
        # Calculate mortality rate percentage based on other fields
        # Adjust the formula according to your specific calculation, mentioned in report
        if self.preexisting_snail_amount > 0:
            return round( (self.expired_snail_amount / self.preexisting_snail_amount) * 100 , 1)
        else:
            return 0
    
    def __int__(self):
        status = int(self.mortality_rate_percentage)
        return status

    def __str__(self):
        status = str(self.mortality_rate_percentage) + "%"
        return status


@receiver(post_save, sender=SnailMortalityRate)
def update_snailbed_mortality_rate(sender, instance, **kwargs):
    # When a SnailMortalityRate object is created or saved,
    # update the related SnailBed's mortality_rate property
    # use the latest one
    if instance.snail_bed:
        latest_mortality_rate = SnailMortalityRate.objects.filter(snail_bed=instance.snail_bed).aggregate(Max('datetime'))['datetime__max']
        latest_mortality_object = SnailMortalityRate.objects.filter(snail_bed=instance.snail_bed, datetime=latest_mortality_rate).first()

        if latest_mortality_object:
            instance.snail_bed.mortality_rate = latest_mortality_object
            instance.snail_bed.save()

class TimeTakenToMature(models.Model):
    snail_bed = models.OneToOneField(SnailBed, on_delete=models.CASCADE)
    snail_hatched = models.DateTimeField(default=timezone.now)
    snail_matured = models.DateTimeField(default=timezone.now)
    days_to_mature = models.PositiveIntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    @property
    def days_to_mature(self):
        # Calculate the number of days taken to mature based on other fields
        # Adjust the formula according to your specific calculation
        time_difference = self.snail_matured - self.snail_hatched
        return time_difference.days

    def __int__(self):
        status = self.days_to_mature
        return status
    
    def __str__(self):
        status = str(self.days_to_mature) + " days"
        return status

class SnailPerformance(models.Model):
    snail_bed = models.OneToOneField(SnailBed, on_delete=models.CASCADE)

    snail_feed = models.ForeignKey(SnailFeed, on_delete=models.CASCADE)
    snail_hatch_rate = models.ForeignKey(SnailHatchRate, on_delete=models.CASCADE)
    snail_mortality_rate = models.ForeignKey(SnailMortalityRate, on_delete=models.CASCADE)
    time_taken_to_mature = models.ForeignKey(TimeTakenToMature, on_delete=models.CASCADE)
    normalized_hatch_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    normalized_mortality_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    expected_time_to_maturity = models.PositiveIntegerField(null=True, blank=True)
    bed_performance = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    @property
    def bed_performance(self):
        hatch_rate_percentage = int(self.snail_hatch_rate)
        mortality_rate_percentage = int(self.snail_mortality_rate)
        bed_performance = (hatch_rate_percentage - mortality_rate_percentage) * (int(self.expected_time_to_maturity) / int(self.time_taken_to_mature))
        return int(bed_performance)

    def __int__(self):
        status = self.bed_performance
        return status

    def __str__(self):
        status = str(self.bed_performance) + "%"
        return status


class ForecastedHatchRate(models.Model):
    snail_bed = models.OneToOneField(SnailBed, on_delete=models.CASCADE)
    forecasted_value = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    forecasted_value_pyaf = PickledObjectField()

    # @staticmethod
    # def calculate_forecast():
    #     # Get all previous records
    #     previous_records = SnailHatchRate.objects.all()

    #     # Calculate the forecasted value based on previous records (example: average)
    #     total_records = previous_records.count()
    #     if total_records > 0:
    #         sum_hatch_rate = sum([record.hatch_rate_percentage for record in previous_records])
    #         forecasted_value = sum_hatch_rate / total_records
    #     else:
    #         forecasted_value = 0

    #     return forecasted_value


    # @staticmethod
    # def calculate_forecast_pyaf():
    #     # Get all previous records
    #     previous_records = SnailHatchRate.objects.all()
    #     # Create a dataframe from previous records
    #     data = pd.DataFrame(list(previous_records.values('hatch_date', 'newly_hatched_snails')))
    #     # Rename columns to match PyAF input requirements
    #     data.rename(columns={'hatch_date': 'ds', 'newly_hatched_snails': 'y'}, inplace=True)

    #     m = NeuralProphet()
    #     metrics = m.fit(data, freq="D")
    #     forecast1 = m.predict(data)

    #     # m = NeuralProphet()
    #     future = m.make_future_dataframe(data, periods=60)
    #     forecast2 = m.predict(future)


    #     #according to https://github.com/ourownstory/neural_prophet
    #     combined = pd.concat([forecast1, forecast2])
    #     fig_forecast = m.plot(combined)
    #     forecasted_value_pyaf = fig_forecast
    #     return forecasted_value_pyaf

    @staticmethod
    def calculate_forecast(snail_bed):
        # Get all previous records for the specific snail_bed
        previous_records = SnailHatchRate.objects.filter(snail_bed=snail_bed)

        # Calculate the forecasted value based on previous records (example: average)
        total_records = previous_records.count()
        if total_records > 0:
            sum_hatch_rate = sum([record.hatch_rate_percentage for record in previous_records])
            forecasted_value = sum_hatch_rate / total_records
        else:
            forecasted_value = 0

        return forecasted_value

    @staticmethod
    def calculate_forecast_pyaf(snail_bed):
        # Get all previous records for the specific snail_bed
        previous_records = SnailHatchRate.objects.filter(snail_bed=snail_bed)
        # Create a dataframe from previous records
        data = pd.DataFrame(list(previous_records.values('hatch_date', 'newly_hatched_snails')))
        # Rename columns to match PyAF input requirements
        data.rename(columns={'hatch_date': 'ds', 'newly_hatched_snails': 'y'}, inplace=True)

        m = NeuralProphet()
        metrics = m.fit(data, freq="D")
        forecast1 = m.predict(data)

        # m = NeuralProphet()
        future = m.make_future_dataframe(data, periods=60)
        forecast2 = m.predict(future)

        # according to https://github.com/ourownstory/neural_prophet
        combined = pd.concat([forecast1, forecast2])
        fig_forecast = m.plot(combined)
        forecasted_value_pyaf = fig_forecast
        return forecasted_value_pyaf

    def save(self, *args, **kwargs):
        self.forecasted_value = self.calculate_forecast(self.snail_bed)
        self.forecasted_value_pyaf = self.calculate_forecast_pyaf(self.snail_bed)

        super().save(*args, **kwargs)

    # def save(self, *args, **kwargs):
    #     self.forecasted_value = self.calculate_forecast()
    #     self.forecasted_value_pyaf = self.calculate_forecast_pyaf()

    #     super().save(*args, **kwargs)

