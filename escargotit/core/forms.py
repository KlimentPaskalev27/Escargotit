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


class RegisterForm(UserCreationForm):
    # Define extra fields
    business_name = forms.CharField(label='business_name', required=True)
    company_tax_code = forms.CharField(label='company_tax_code', required=True)

    def save(self, *args, **kwargs):
        user = super().save(*args, **kwargs)
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.save()  # Save the User object

        # get the values from the extra fields and clean them
        business_name = self.cleaned_data.get('business_name')
        company_tax_code = self.cleaned_data.get('company_tax_code')

        # create a new AdminUser object with this data
        profile = AdminUser.objects.create(
            user=user,
            first_name=user.first_name,
            last_name=user.last_name,
            business_name = business_name,
            company_tax_code=company_tax_code,
            )
        profile.save()  # Save the AdminUser object to the database

        return user

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'business_name', 'company_tax_code'] #password is added as field by default + pass confirmation


class EmployeePermissionForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['user_permissions']



class EmployeeCreationForm(UserCreationForm):
    def __init__(self, admin, *args, **kwargs):
        super(EmployeeCreationForm, self).__init__(*args, **kwargs)
        self.admin = admin  # Store the admin object that is passed by our view
    
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
        employee = EmployeeUser.objects.create(user = user, admin=self.admin)
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


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and not self.user_cache:
            raise ValidationError("Invalid username. Please try again.")

        if username and password and self.user_cache is not None and not self.user_cache.check_password(password):
            raise ValidationError("Invalid password. Please try again.")


class AccountDeletionForm(forms.Form):
    confirm = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )

