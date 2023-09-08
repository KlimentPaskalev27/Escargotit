from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model  # Use get_user_model to reference the user model


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

class SnailBedForm(forms.ModelForm):
    class Meta:
        model = SnailBed
        fields = ['bed_name']


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email'] #password is added as field by default + pass confirmation

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if get_user_model().objects.filter(email=email).exists():
            raise ValidationError("This email address is already in use.")
        return email

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        return password

    def clean_password2(self):
        password = self.cleaned_data.get('password2')
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        return password

    def save(self, commit=True, *args, **kwargs):
        user = super().save(commit=False)  # Create the user object but don't save it yet
        user.set_password(self.cleaned_data['password1'])  # Set the password
        if commit:
            user.save()
        # now create profile
        user = super().save(*args, **kwargs)
        profile = Profile.objects.create(user = user)
        profile.save()
        return user

    # def save(self, *args, **kwargs):
    #     user = super().save(*args, **kwargs)
    #     profile = Profile.objects.create(user = user)
    #     profile.save()
    #     return user



class RegisterForm(UserCreationForm):
    def save(self, *args, **kwargs):
        user = super().save(*args, **kwargs)
        profile = Profile.objects.create(user = user)
        profile.save()
        return user

    class Meta:
        model = User
        fields = ['username', 'email'] #password is added as field by default + pass confirmation
