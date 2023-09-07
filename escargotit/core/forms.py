from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class SnailFeedForm(forms.ModelForm):
    class Meta:
        model = SnailFeed
        fields = ['snail_bed', 'consumed_on', 'grams_feed_given']

class SnailHatchRateForm(forms.ModelForm):
    class Meta:
        model = SnailHatchRate
        fields = ['snail_bed', 'newly_hatched_snails', 'datetime']

class SnailMortalityRateForm(forms.ModelForm):
    class Meta:
        model = SnailMortalityRate
        fields = ['snail_bed', 'expired_snail_amount', 'datetime']

class TimeTakenToMatureForm(forms.ModelForm):
    class Meta:
        model = TimeTakenToMature
        fields = ['snail_bed', 'snail_hatched', 'snail_matured', 'snails_matured_count']

class SnailBedPerformanceForm(forms.ModelForm):
    class Meta:
        model = SnailBedPerformance
        fields = ['expected_time_to_maturity']







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



