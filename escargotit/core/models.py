import numpy as np
import pandas as pd
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from neuralprophet import NeuralProphet
from picklefield.fields import PickledObjectField
from django.contrib.auth.models import User


class SnailFeed(models.Model):
    consumed_on = models.DateTimeField()
    grams_feed_given = models.IntegerField()

    def __int__(self):
        status = self.grams_feed_given
        return status

    def __str__(self):
        status = str(self.grams_feed_given) + " grams"
        return status

class SnailBirthRate(models.Model):
    birth_date = models.DateField()
    preexisting_snail_amount = models.IntegerField()
    newly_hatched_snails = models.IntegerField()
    birth_rate_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.preexisting_snail_amount and self.newly_hatched_snails:
           self.birth_rate_percentage = (self.newly_hatched_snails / self.preexisting_snail_amount) * 100
        super().save(*args, **kwargs)

    @property
    def birth_rate_percentage(self):
        # Calculate birth rate percentage based on other fields
        # Adjust the formula according to your specific calculation
        if self.preexisting_snail_amount > 0:
            return (self.newly_hatched_snails / self.preexisting_snail_amount) * 100
        else:
            return 0

    def __int__(self):
        return int(self.birth_rate_percentage)

    def __str__(self):
        status = str(self.birth_rate_percentage) + "%"
        return status


class SnailMortalityRate(models.Model):
    preexisting_snail_amount = models.IntegerField()
    expired_snail_amount = models.IntegerField()
    mortality_rate_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.preexisting_snail_amount and self.expired_snail_amount:
            self.mortality_rate_percentage = (self.expired_snail_amount / self.preexisting_snail_amount) * 100
        super().save(*args, **kwargs)

    @property
    def mortality_rate_percentage(self):
        # Calculate mortality rate percentage based on other fields
        # Adjust the formula according to your specific calculation
        if self.preexisting_snail_amount > 0:
            return (self.expired_snail_amount / self.preexisting_snail_amount) * 100
        else:
            return 0
    
    def __int__(self):
        status = int(self.mortality_rate_percentage)
        return status

    def __str__(self):
        status = str(self.mortality_rate_percentage) + "%"
        return status

class TimeTakenToMature(models.Model):
    snail_hatched = models.DateTimeField()
    snail_matured = models.DateTimeField()
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
    snail_feed = models.ForeignKey(SnailFeed, on_delete=models.CASCADE)
    snail_birth_rate = models.ForeignKey(SnailBirthRate, on_delete=models.CASCADE)
    snail_mortality_rate = models.ForeignKey(SnailMortalityRate, on_delete=models.CASCADE)
    time_taken_to_mature = models.ForeignKey(TimeTakenToMature, on_delete=models.CASCADE)
    normalized_birth_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    normalized_mortality_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    expected_time_to_maturity = models.PositiveIntegerField(null=True, blank=True)
    bed_performance = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    @property
    def bed_performance(self):
        birth_rate_percentage = int(self.snail_birth_rate)
        mortality_rate_percentage = int(self.snail_mortality_rate)
        bed_performance = (birth_rate_percentage - mortality_rate_percentage) * (int(self.expected_time_to_maturity) / int(self.time_taken_to_mature))
        return int(bed_performance)

    def __int__(self):
        status = self.bed_performance
        return status

    def __str__(self):
        status = str(self.bed_performance) + "%"
        return status


class ForecastedBirthRate(models.Model):
    forecasted_value = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    forecasted_value_pyaf = PickledObjectField()

    @staticmethod
    def calculate_forecast():
        # Get all previous SnailBirthRate records
        previous_records = SnailBirthRate.objects.all()

        # Calculate the forecasted value based on previous records (Example: average)
        total_records = previous_records.count()
        if total_records > 0:
            sum_birth_rate = sum([record.birth_rate_percentage for record in previous_records])
            forecasted_value = sum_birth_rate / total_records
        else:
            forecasted_value = 0

        return forecasted_value


    @staticmethod
    def calculate_forecast_pyaf():
        # Get all previous SnailBirthRate records
        previous_records = SnailBirthRate.objects.all()
        # Create a dataframe from previous records
        data = pd.DataFrame(list(previous_records.values('birth_date', 'newly_hatched_snails')))
        # Rename columns to match PyAF input requirements
        data.rename(columns={'birth_date': 'ds', 'newly_hatched_snails': 'y'}, inplace=True)

        m = NeuralProphet()
        metrics = m.fit(data, freq="D")
        forecast1 = m.predict(data)

        # m = NeuralProphet()
        future = m.make_future_dataframe(data, periods=60)
        forecast2 = m.predict(future)


        #according to https://github.com/ourownstory/neural_prophet
        combined = pd.concat([forecast1, forecast2])
        fig_forecast = m.plot(combined)
        forecasted_value_pyaf = fig_forecast
        return forecasted_value_pyaf

    def save(self, *args, **kwargs):
        self.forecasted_value = self.calculate_forecast()
        self.forecasted_value_pyaf = self.calculate_forecast_pyaf()

        super().save(*args, **kwargs)



class SnailBed(models.Model):
    # Fields specific to SnailBed
    bed_name = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=255)
    # Add any other fields specific to SnailBed here

    # Inherit fields and relationships from other models
    snail_feed = models.ForeignKey('SnailFeed', on_delete=models.CASCADE)
    snail_birth_rate = models.ForeignKey('SnailBirthRate', on_delete=models.CASCADE)
    snail_mortality_rate = models.ForeignKey('SnailMortalityRate', on_delete=models.CASCADE)
    time_taken_to_mature = models.ForeignKey('TimeTakenToMature', on_delete=models.CASCADE)
    snail_performance = models.ForeignKey('SnailPerformance', on_delete=models.CASCADE)
    forecasted_birth_rate = models.ForeignKey('ForecastedBirthRate', on_delete=models.CASCADE)

    # Add any additional fields or methods specific to SnailBed here

    # User reference
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.bed_name


