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
from decimal import Decimal

class AdminUser(models.Model):
    can_create_snailbed = models.BooleanField(default=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class EmployeeUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    can_create_snailbed = models.BooleanField(default=False)
    def __str__(self):
        return self.user.username

class SnailBed(models.Model):
    bed_name = models.CharField(max_length=100, unique=False, null=True, blank=True)
    user = models.ForeignKey(AdminUser, on_delete=models.SET_NULL, null=True, blank=True, db_constraint=False)
    employee = models.ForeignKey(EmployeeUser, on_delete=models.SET_NULL, null=True, blank=True, db_constraint=False)
    snail_amount = models.IntegerField(null=True, blank=True)
    hatch_rate = models.ForeignKey('SnailHatchRate', on_delete=models.SET_NULL, null=True, blank=True)
    mortality_rate = models.ForeignKey('SnailMortalityRate', on_delete=models.SET_NULL, null=True, blank=True)

    def can_create(self, user):
        return user.has_perm('add_snailbed')

    def can_delete(self, user):
        return user.has_perm('delete_snailbed')

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
    snail_bed = models.ForeignKey(SnailBed, on_delete=models.CASCADE)
    consumed_on = models.DateTimeField(default=timezone.now)
    grams_feed_given = models.IntegerField()

    def __int__(self):
        status = self.grams_feed_given
        return status

    def __str__(self):
        status = str(self.grams_feed_given) + " grams"
        return status

class SnailHatchRate(models.Model):
    snail_bed = models.ForeignKey(SnailBed, on_delete=models.CASCADE)
    preexisting_snail_amount = models.IntegerField(null=True, blank=True, default=0)
    newly_hatched_snails = models.IntegerField()
    hatch_rate_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    datetime = models.DateTimeField(default=timezone.now)

    @property
    def hatch_rate_percentage(self):
        # Calculate hatch rate percentage based on other fields
        # Adjust the formula according to your specific calculation
        if self.preexisting_snail_amount > 0:
            return round( (self.newly_hatched_snails / self.preexisting_snail_amount) * 100 , 1)
        else:
            return 0

    def save(self, *args, **kwargs):
        # Calculate the new snail_amount for the associated SnailBed
        self.preexisting_snail_amount = self.snail_bed.snail_amount

        if self.preexisting_snail_amount is not None and self.newly_hatched_snails is not None:
            # Calculate the new snail_amount by adding the newly hatched snails
            new_snail_amount = self.preexisting_snail_amount + self.newly_hatched_snails

            # Update the SnailBed's snail_amount field
            self.snail_bed.snail_amount = new_snail_amount
            self.snail_bed.save()

        super().save(*args, **kwargs)

    def __float__(self):
        status = self.hatch_rate_percentage
        return status

    def __int__(self):
        return int(self.hatch_rate_percentage)

    def __str__(self):
        status = str(self.hatch_rate_percentage) + "%"
        return status

@receiver(post_save, sender=SnailHatchRate)
def update_snailbed_hatch_rate(sender, instance, **kwargs):
    # When a SnailHatchRate object is created or saved,
    # update the related SnailBed's hatch_rate property
    # use the latest one
    if instance.snail_bed:
        latest_hatch_rate = SnailHatchRate.objects.filter(snail_bed=instance.snail_bed).aggregate(Max('datetime'))['datetime__max']
        latest_hatch_object = SnailHatchRate.objects.filter(snail_bed=instance.snail_bed, datetime=latest_hatch_rate).first()

        if latest_hatch_object:
            instance.snail_bed.hatch_rate = latest_hatch_object
            instance.snail_bed.save()

class SnailMortalityRate(models.Model):
    snail_bed = models.ForeignKey(SnailBed, on_delete=models.CASCADE)
    preexisting_snail_amount = models.IntegerField(null=True, blank=True)
    expired_snail_amount = models.IntegerField(default=0)
    mortality_rate_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    datetime = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.preexisting_snail_amount = self.snail_bed.snail_amount

        if self.preexisting_snail_amount is not None and self.expired_snail_amount is not None:
            new_snail_amount = self.preexisting_snail_amount - self.expired_snail_amount
            self.snail_bed.snail_amount = new_snail_amount
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

    def __float__(self):
        status = self.mortality_rate_percentage
        return status
    
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
    snail_bed = models.ForeignKey(SnailBed, on_delete=models.CASCADE)
    snail_hatched = models.DateTimeField(default=timezone.now)
    snail_matured = models.DateTimeField(default=timezone.now)
    snails_matured_count = models.IntegerField(default=0)
    days_to_mature = models.PositiveIntegerField(null=True, blank=True)
    period = models.DurationField(null=True, blank=True)
    maturity_percentage = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.snail_bed:
            # Calculate the period between snail_matured and snail_hatched
            time_difference = self.snail_matured - self.snail_hatched
            self.period = time_difference

            # Update the snails_matured_count based on snails hatched within the period
            snails_hatched_within_period = SnailHatchRate.objects.filter(
                snail_bed=self.snail_bed,
                datetime__gte=self.snail_hatched,
                datetime__lte=self.snail_matured
            ).aggregate(models.Sum('newly_hatched_snails'))['newly_hatched_snails__sum']

            if snails_hatched_within_period is not None:
                self.snails_matured_count = snails_hatched_within_period

                # Calculate the maturity percentage
                total_snails_hatched_within_period = SnailHatchRate.objects.filter(
                    snail_bed=self.snail_bed,
                    datetime__gte=self.snail_hatched,
                    datetime__lte=self.snail_matured
                ).aggregate(models.Sum('preexisting_snail_amount'))['preexisting_snail_amount__sum']

                if total_snails_hatched_within_period:
                    self.maturity_percentage = round( (self.snails_matured_count / total_snails_hatched_within_period) * 100 , 1)

        super().save(*args, **kwargs)

    @property
    def days_to_mature(self):
        if self.period:
            # Calculate the number of days taken to mature based on other fields
            # Adjust the formula according to your specific calculation
            time_difference = self.snail_matured - self.snail_hatched
            return time_difference.days
        return None

    def __int__(self):
        status = self.days_to_mature
        return status
    
    def __str__(self):
        if self.maturity_percentage and self.days_to_mature:
            return str(self.maturity_percentage) + "% of snail bed has reached maturity in " + str(self.days_to_mature) + " days"
        return "N/A"

class SnailBedPerformance(models.Model):
    snail_bed = models.ForeignKey(SnailBed, on_delete=models.CASCADE)

    snail_feed = models.ForeignKey(SnailFeed, on_delete=models.CASCADE)
    snail_hatch_rate = models.ForeignKey(SnailHatchRate, on_delete=models.CASCADE)
    snail_mortality_rate = models.ForeignKey(SnailMortalityRate, on_delete=models.CASCADE)
    time_taken_to_mature = models.ForeignKey(TimeTakenToMature, on_delete=models.CASCADE)

    reproduction_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    expected_time_to_maturity = models.PositiveIntegerField(null=True, blank=True)

    bed_performance = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    @property
    def reproduction_rate(self):
        if self.snail_hatch_rate and self.snail_mortality_rate and self.time_taken_to_mature:
            normalized_hatch_rate = float(self.snail_hatch_rate) * 100
            normalized_mortality_rate = float(self.snail_mortality_rate) * 100
            normalized_reproduction_rate = normalized_hatch_rate - normalized_mortality_rate
            reproduction_rate_factor = round(normalized_reproduction_rate / 100, 2)
            return reproduction_rate_factor
        return None

    @property
    def bed_performance(self):
        if self.reproduction_rate and self.expected_time_to_maturity and self.time_taken_to_mature.days_to_mature > 0:
            maturity_factor = self.expected_time_to_maturity / self.time_taken_to_mature.days_to_mature
            performance = self.reproduction_rate * maturity_factor
            return round(performance, 2)
        else:
            maturity_factor = 1.0

            performance = self.reproduction_rate * maturity_factor
            return round(performance, 2)  # Convert to percentage and round to 2 decimal places
        return None

    def __int__(self):
        status = self.bed_performance
        return status

    def __str__(self):
        status = str( self.bed_performance ) + "%"
        return status

class ForecastedHatchRate(models.Model):
    snail_bed = models.ForeignKey(SnailBed, on_delete=models.CASCADE)
    forecasted_value = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    forecasted_value_pyaf = PickledObjectField()

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
        data = pd.DataFrame(list(previous_records.values('datetime', 'newly_hatched_snails')))
        # Rename columns to match PyAF input requirements
        data.rename(columns={'datetime': 'ds', 'newly_hatched_snails': 'y'}, inplace=True)

        m = NeuralProphet()
        m.fit(data, freq="D")
        forecast1 = m.predict(data)
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

    def __float__(self):
        status = self.forecasted_value
        return status

    def __int__(self):
        status = int(self.forecasted_value)
        return status

    def __str__(self):
        status = str(self.forecasted_value) + "%"
        return status

