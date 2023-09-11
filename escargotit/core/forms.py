from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model  # Use get_user_model to reference the user model

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
        fields = ['snail_hatched', 'snail_matured', 'snails_matured_count']


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
        profile = AdminUser.objects.create(user = user)
        profile.save()
        return user



class RegisterForm(UserCreationForm):
    def save(self, *args, **kwargs):
        user = super().save(*args, **kwargs)
        profile = AdminUser.objects.create(user = user)
        profile.save()
        return user

    # Define extra fields
    business_name = forms.CharField(label='business_name', required=True)
    company_tax_code = forms.CharField(label='company_tax_code', required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'business_name', 'company_tax_code'] #password is added as field by default + pass confirmation



class EmployeeCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

class EmployeePermissionForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['user_permissions']



class EmployeeCreationForm(UserCreationForm):
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
        # now create employee
        user = super().save(*args, **kwargs)
        employee = EmployeeUser.objects.create(user = user)
        employee.save()
        return user


class SnailHatchRateForm(forms.ModelForm):
    class Meta:
        model = SnailHatchRate
        fields = ['newly_hatched_snails', 'datetime']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['newly_hatched_snails'].label = 'Newly Hatched Snails'
        self.fields['datetime'].label = 'Date and Time'
        #self.fields['datetime'].widget = forms.TextInput(attrs={'type': 'datetime-local'})


class SnailMortalityRateForm(forms.ModelForm):
    class Meta:
        model = SnailMortalityRate
        fields = ['expired_snail_amount', 'datetime']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['expired_snail_amount'].label = 'Expired Snail Amount'
        self.fields['datetime'].label = 'Date and Time'
        #self.fields['datetime'].widget = forms.TextInput(attrs={'type': 'datetime-local'})

class SnailFeedForm(forms.ModelForm):
    class Meta:
        model = SnailFeed
        fields = ['grams_feed_given', 'consumed_on']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['grams_feed_given'].label = 'Grams of Feed Given'
        self.fields['consumed_on'].label = 'Date'


class DeleteEmployeeForm(forms.Form):
    employee_to_delete = forms.ModelChoiceField(
        queryset=EmployeeUser.objects.all(),
        label='Select Employee to Delete'
    )

    def clean_employee_to_delete(self):
        employee_to_delete = self.cleaned_data.get('employee_to_delete')
        
        assigned_beds = SnailBed.objects.filter(employee=employee_to_delete)
        if assigned_beds.exists():
            bed_names = ', '.join([bed.bed_name for bed in assigned_beds])
            raise forms.ValidationError(
                f'Employee is assigned to one or more Snail Beds. Unassign them first before deleting. Here is a list of the beds: {bed_names}.'
            )
        
        return employee_to_delete

class EmployeeUserForm(forms.ModelForm):
    class Meta:
        model = EmployeeUser
        fields = ['can_create_snailbed']

class EmployeeChangeForm(UserChangeForm):

    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput, required=False)
    new_password2 = forms.CharField(label='Confirm New Password', widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_new_password2(self):
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password2')
        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError('The two password fields must match.')
        return new_password2