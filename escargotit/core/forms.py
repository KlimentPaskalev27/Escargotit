from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class SnailFeedForm(forms.ModelForm):
    class Meta:
        model = SnailFeed
        fields = ['consumed_on', 'grams_feed_given']

class SnailHatchRateForm(forms.ModelForm):
    class Meta:
        model = SnailHatchRate
        fields = ['preexisting_snail_amount', 'newly_hatched_snails', 'datetime']

class SnailMortalityRateForm(forms.ModelForm):
    class Meta:
        model = SnailMortalityRate
        fields = ['preexisting_snail_amount', 'expired_snail_amount']

class TimeTakenToMatureForm(forms.ModelForm):
    class Meta:
        model = TimeTakenToMature
        fields = ['snail_hatched', 'snail_matured']

class SnailBedPerformanceForm(forms.ModelForm):
    class Meta:
        model = SnailBedPerformance
        fields = ['snail_feed', 'snail_hatch_rate', 'snail_mortality_rate', 'time_taken_to_mature', 'expected_time_to_maturity']







class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email address is already in use.")
        return email

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        return password



