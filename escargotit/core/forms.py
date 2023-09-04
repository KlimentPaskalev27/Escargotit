from django import forms
from .models import *

class SnailFeedForm(forms.ModelForm):
    class Meta:
        model = SnailFeed
        fields = ['consumed_on', 'grams_feed_given']

class SnailBirthRateForm(forms.ModelForm):
    class Meta:
        model = SnailBirthRate
        fields = ['birth_date', 'preexisting_snail_amount', 'newly_hatched_snails']

class SnailMortalityRateForm(forms.ModelForm):
    class Meta:
        model = SnailMortalityRate
        fields = ['preexisting_snail_amount', 'expired_snail_amount']

class TimeTakenToMatureForm(forms.ModelForm):
    class Meta:
        model = TimeTakenToMature
        fields = ['snail_hatched', 'snail_matured']

class SnailPerformanceForm(forms.ModelForm):
    class Meta:
        model = SnailPerformance
        fields = ['snail_feed', 'snail_birth_rate', 'snail_mortality_rate', 'time_taken_to_mature', 'expected_time_to_maturity']









