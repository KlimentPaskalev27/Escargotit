import pandas as pd
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from pyaf import ForecastEngine

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
    preexisting_snail_amount = models.IntegerField()
    newly_hatched_snails = models.IntegerField()
    birth_rate_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def save(self, *args, **kwargs):
        # if self.preexisting_snail_amount and self.newly_hatched_snails:
        #     self.birth_rate_percentage = (self.newly_hatched_snails / self.preexisting_snail_amount) * 100
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
        # if self.snail_hatched and self.snail_matured:
        #     time_difference = self.snail_matured - self.snail_hatched
        #     self.days_to_mature = time_difference.days
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
        # if self.snail_birth_rate and self.snail_mortality_rate:
        #     maximum_birth_rate = SnailBirthRate.objects.order_by('-birth_rate_percentage').first().birth_rate_percentage
        #     maximum_mortality_rate = SnailMortalityRate.objects.order_by('-mortality_rate_percentage').first().mortality_rate_percentage

        #     if maximum_birth_rate and maximum_birth_rate > 0:
        #         self.normalized_birth_rate = (self.snail_birth_rate.birth_rate_percentage / maximum_birth_rate) * 100

        #     if maximum_mortality_rate and maximum_mortality_rate > 0:
        #         self.normalized_mortality_rate = (self.snail_mortality_rate.mortality_rate_percentage / maximum_mortality_rate) * 100

        # self.bed_performance = (birth_rate_percentage - mortality_rate_percentage) * ( 1 * (expected_time_to_maturity / time_taken_to_mature))
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
    forecasted_value_pyaf = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

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
        data = pd.DataFrame(list(previous_records.values('date', 'birth_rate')))

        # Rename columns to match PyAF input requirements
        data.rename(columns={'date': 'Time', 'birth_rate': 'Signal'}, inplace=True)

        # Initialize the PyAF ForecastEngine
        engine = ForecastEngine()

        # Fit the model and make the forecast
        forecast_result = engine.fit(data, 'Time', 'Signal', 1)
        forecast_df = forecast_result.forecast(forecast_result.data, steps=1)

        # Get the forecasted value
        forecasted_value_pyaf = forecast_df['Signal_Forecast'].iloc[-1]

        return forecasted_value_pyaf

@receiver(post_save, sender=SnailBirthRate)
def update_forecasted_birth_rate(sender, instance, **kwargs):
    # Whenever a new SnailBirthRate record is added, update the ForecastedBirthRate record
    forecasted_birth_rate = ForecastedBirthRate.objects.first()
    if forecasted_birth_rate:
        forecasted_birth_rate.forecasted_value_pyaf = ForecastedBirthRate.calculate_forecast_pyaf()
        forecasted_birth_rate.save()
    else:
        ForecastedBirthRate.objects.create(forecasted_value_pyaf=ForecastedBirthRate.calculate_forecast_pyaf())

@receiver(post_save, sender=SnailBirthRate)
def update_forecasted_birth_rate(sender, instance, **kwargs):
    # Whenever a new SnailBirthRate record is added, update the ForecastedBirthRate record
    forecasted_birth_rate = ForecastedBirthRate.objects.first()
    if forecasted_birth_rate:
        forecasted_birth_rate.forecasted_value = ForecastedBirthRate.calculate_forecast()
        forecasted_birth_rate.save()
    else:
        ForecastedBirthRate.objects.create(forecasted_value=ForecastedBirthRate.calculate_forecast())