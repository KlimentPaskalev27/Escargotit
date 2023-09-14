#Import standard library modules first
from io import BytesIO
import base64
import random # generate data for dummy data population
import datetime
from datetime import timedelta # turn integers into days, weeks.. 

#Import third-party libraries 
import matplotlib
# avoid error crashes runtime - async handler deleted by the wrong thread
# matplotlib uses tkinter by default, overide that to avoid exception crash
# https://stackoverflow.com/questions/27147300/matplotlib-tcl-asyncdelete-async-handler-deleted-by-the-wrong-thread
matplotlib.use('Agg')
from matplotlib import pyplot as plt # plot graphs
# https://scipy.org/install/
from scipy.stats import pearsonr  # For calculating correlation coefficient

#Django modules and classes
from django.contrib import messages  # the messages module allows success, info, and error messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash  # auth_hash makes it possible to update passwords
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy  # used to redirect back to the request URL
from django.views.generic import CreateView, ListView
from rest_framework import viewsets

# custom forms, models, and other local modules
from .forms import *
from .models import *
from .serializers import *
from .faq_data import faq_data  # Import the faq_data from the module


@login_required(login_url='login')
def dashboard(request):

    is_admin=False #conditions for the template to render stuff

    current_user = AdminUser.objects.filter(user=request.user).first()
    if isinstance(current_user, AdminUser):
        is_admin=True
        
        # Handle the POST request to add a new SnailBed object
        if request.method == 'POST':
            # Create a new SnailBed object based on the form data
            new_snail_bed = SnailBed(user=current_user)
            new_snail_bed.save()  # Save the new SnailBed to the database

            # After processing the POST request, redirect to the dashboard page using the GET method
            return HttpResponseRedirect(request.path_info)  # Redirect to the same page (GET request)

        # Retrieve all SnailBeds for the logged-in user
        snail_beds = SnailBed.objects.filter(user=current_user).order_by('-id') # reverse id is to show the newest on top of the page

    elif isinstance(EmployeeUser.objects.filter(user=request.user).first(), EmployeeUser):
        current_user = EmployeeUser.objects.filter(user=request.user).first()
        snail_beds = SnailBed.objects.filter(employee=current_user).order_by('-id')
    else:
        snail_beds = SnailBed.objects.filter(user=current_user).order_by('-id')

    snail_bed_count = snail_beds.count()

    context = {
        'current_user': current_user,
        'snail_beds': snail_beds,
        'snail_bed_count': snail_bed_count,
        'is_admin': is_admin,
    }

    return render(request, 'dashboard.html',context)

@login_required(login_url='login')
def index(request):
    return render(request, 'index.html')

@login_required(login_url='login')
def delete_all_snailbeds(request):
    current_user = AdminUser.objects.filter(user=request.user).first()
    # Assuming you have a user-based association in your SnailBed model
    # You should adjust this logic based on your model structure
    SnailBed.objects.filter(user=current_user).delete()
    return redirect('dashboard')  # Redirect back to the dashboard 

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']

            # Check if a user with the same username already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists. Please choose a different username.')
            else:
                form.save()
                messages.success(request, 'Registration successful. You can now log in.')
                return redirect('login')
    else:
        form = RegisterForm()
    
    return render(request, 'registration/register.html', {'form': form})

# use DJango LoginView ready form class
class LoginFormView(LoginView):
    template_name = 'registration/login.html'
    def form_valid(self, form):
        super().form_valid(form)
        return redirect(reverse_lazy('dashboard'))

def logout_view(request):
    logout(request)
    # Redirect to a logout success page or login page
    return redirect('login')

@login_required(login_url='login')
def user_settings(request):
    
    user = request.user

    if request.method == 'POST':
        user_form = UserChangeForm(request.POST, instance=user)
        password_form = PasswordChangeForm(user, request.POST)

        if user_form.is_valid():
            user_form.save()
            # Update session auth hash to prevent automatic logout
            update_session_auth_hash(request, user)
            return redirect('user_settings')  # Redirect after successful update

        if password_form.is_valid():
            password_form.save()
            # Update session auth hash after password change
            update_session_auth_hash(request, user)
            return redirect('user_settings')  # Redirect after successful password change
    else:
        user_form = UserChangeForm(instance=user)
        password_form = PasswordChangeForm(user)

    return render(request, 'registration/user_settings.html', {'user_form': user_form, 'password_form': password_form})

@login_required(login_url='login')
def delete_account(request):
    if request.method == 'POST':
        form = AccountDeletionForm(request.POST)
        if form.is_valid() and form.cleaned_data['confirm']:
            # Delete the user's account
            request.user.delete()
            logout(request)  # Log out the user after deleting their account
            return redirect('login')  # Redirect to the login page or another suitable URL
    else:
        form = AccountDeletionForm()
    
    return render(request, 'registration/delete_account.html', {'form': form})

def contact(request):
    return render(request, 'company/contact.html')

def about(request):
    return render(request, 'company/about.html')

def terms(request):
    return render(request, 'company/terms.html')

def cookies(request):
    return render(request, 'company/cookies.html')

def privacy(request):
    return render(request, 'company/privacy.html')

def faqs(request):
    return render(request, 'company/faqs.html', {'faq_data': faq_data})

def home(request):
    return render(request, 'company/home.html')

@login_required(login_url='login')
def barchart(request, snail_bed_id):
    snail_bed = get_object_or_404(SnailBed, pk=snail_bed_id)

    # Retrieve the combined data
    snail_feeds = SnailFeed.objects.filter(snail_bed=snail_bed).order_by('consumed_on')
    hatch_rates = SnailHatchRate.objects.filter(snail_bed=snail_bed).order_by('datetime')
    mortality_rates = SnailMortalityRate.objects.filter(snail_bed=snail_bed).order_by('datetime')
    maturity_rates = TimeTakenToMature.objects.filter(snail_bed=snail_bed).order_by('snail_matured')

    # Check if there are enough data points for correlation calculation
    if len(snail_feeds) < 3 or len(hatch_rates) < 3 or len(mortality_rates) < 3 or len(maturity_rates) < 3:
        messages.error(request, "There are not enough data points for correlation calculation. Snail Bed should have at least 2 logs for each data field.")
        return redirect('dashboard')  # Redirect to a suitable page

    # Extract grams feed given and hatch rates
    grams_feed_given = [entry.grams_feed_given for entry in snail_feeds]
    hatch_rates_percentage = [entry.hatch_rate_percentage for entry in hatch_rates]
    mortality_rates_percentage = [entry.mortality_rate_percentage for entry in mortality_rates]
    maturity_percentage = [entry.maturity_percentage for entry in maturity_rates]

    # Calculate percentage change for grams feed given
    grams_feed_change = [0]  # Initial value is 0
    for i in range(1, len(grams_feed_given)):
        percentage_change = ((grams_feed_given[i] - grams_feed_given[i - 1]) / grams_feed_given[i - 1]) * 100
        grams_feed_change.append(percentage_change)

    # Calculate percentage change for hatch rates
    hatch_rate_change = [0]  # Initial value is 0
    for i in range(1, len(hatch_rates_percentage)):
        if hatch_rates_percentage[i - 1] != 0:
            percentage_change = ((hatch_rates_percentage[i] - hatch_rates_percentage[i - 1]) / hatch_rates_percentage[i - 1]) * 100
        else:
            # Handle the case when the denominator is zero
            percentage_change = 0  # Set percentage_change to 0 or another appropriate value
        hatch_rate_change.append(percentage_change)

    # Calculate percentage change for mortality rates
    mortality_rate_change = [0]  # Initial value is 0
    for i in range(1, len(mortality_rates_percentage)):
        if mortality_rates_percentage[i - 1] != 0:
            percentage_change = ((mortality_rates_percentage[i] - mortality_rates_percentage[i - 1]) / mortality_rates_percentage[i - 1]) * 100
        else:
            # Handle the case when the denominator is zero (optional)
            percentage_change = 0  # Set percentage_change to 0 or another appropriate value
        mortality_rate_change.append(percentage_change)

    # Calculate percentage change for maturity rates
    maturity_rate_change = [0]  # Initial value is 0
    for i in range(1, len(maturity_percentage)):
        if maturity_percentage[i - 1] is not None and maturity_percentage[i] is not None:
            if maturity_percentage[i - 1] != 0:
                percentage_change = ((maturity_percentage[i] - maturity_percentage[i - 1]) / maturity_percentage[i - 1]) * 100
            else:
                # Handle the case when the denominator is zero (optional)
                percentage_change = 0  # Set percentage_change to 0 or another appropriate value
            maturity_rate_change.append(percentage_change)

    # Before plotting, all datasets must have the same lengths in terms of data points to avoid errors
    # check which dataset is the shortest in length. Calculate the minimum length among the four data sets
    min_length = min(len(grams_feed_change), len(hatch_rate_change), len(mortality_rate_change), len(maturity_rate_change))

    # Trim each data set to the minimum length
    grams_feed_change = grams_feed_change[:min_length]
    hatch_rate_change = hatch_rate_change[:min_length]
    mortality_rate_change = mortality_rate_change[:min_length]
    maturity_rate_change = maturity_rate_change[:min_length]

    # Create the overlapping bar chart
    plt.figure(figsize=(12, 6))
    plt.plot(snail_feeds.values_list('consumed_on', flat=True)[:min_length], grams_feed_change, alpha=0.5, label='Grams Feed Change (%)')
    plt.plot(hatch_rates.values_list('datetime', flat=True)[:min_length], hatch_rate_change, alpha=0.5, label='Hatch Rate Change (%)')
    plt.plot(mortality_rates.values_list('datetime', flat=True)[:min_length], mortality_rate_change, alpha=0.5, color='red', label='Mortality Rate (%)')
    plt.plot(maturity_rates.values_list('snail_matured', flat=True)[:min_length], maturity_rate_change, alpha=0.5, color='green', label='Maturity Rate (%)')

    # Calculate the Pearson correlation coefficient
    feed_hatch_correlation_coefficient, _ = pearsonr(grams_feed_change, hatch_rate_change)
    feed_mortality_correlation_coefficient, _ = pearsonr(grams_feed_change, mortality_rate_change)
    feed_maturity_correlation_coefficient, _ = pearsonr(grams_feed_change, maturity_rate_change)
    maturity_mortality_correlation_coefficient, _ = pearsonr(maturity_rate_change, mortality_rate_change)

    # Prepare correlation objects to pass to template to render stats
    correlation_coefficients = [
        {
        "name" : "Feed Given & Hatch Rate",
        "coefficient": round(feed_hatch_correlation_coefficient,2)
        },
        {
        "name" : "Feed Given & Mortality Rate",
        "coefficient": round(feed_mortality_correlation_coefficient,2)
        },
        {
        "name" : "Feed Given & Maturity Rate",
        "coefficient": round(feed_maturity_correlation_coefficient,2)
        },
        {
        "name" : "Maturity Rate & Mortality Rate",
        "coefficient": round(maturity_mortality_correlation_coefficient,2)
        },
    ]

    # Finish graph setup
    plt.xlabel('Date')
    plt.ylabel('Percentage Change (%)')
    plt.title('Overlapping Bar Chart of Percentage Change')
    plt.xticks(rotation=45)
    plt.legend()

    # Save the plot to a BytesIO object
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    # Convert the plot to base64 for embedding in HTML
    plot_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    context = {
        'snail_bed': snail_bed,
        'plot_base64': plot_base64,
        "correlations": correlation_coefficients,
    }

    return render(request, 'barchart.html', context)

@login_required(login_url='login')
def custom_admin_panel(request):
    current_user = AdminUser.objects.filter(user=request.user).first()

    if request.method == 'POST' and 'register_employee' in request.POST:
        form = EmployeeCreationForm(admin=current_user, data=request.POST) # pass current admin
        #form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Employee user {username} has been created.')
            return redirect('custom_admin_panel')
    else:
        form = EmployeeCreationForm(admin=current_user)

    # Add code to handle the assignment of existing employees to snail beds
    if request.method == 'POST' and 'assign_employee' in request.POST:
        snail_bed_id = request.POST.get('snail_bed_id')
        employee_id = request.POST.get('employee_id')
        snail_bed = get_object_or_404(SnailBed, pk=snail_bed_id)
        employee = get_object_or_404(EmployeeUser, pk=employee_id)
        snail_bed.employee = employee
        snail_bed.save()
        messages.success(request, f'Employee {employee.user.username} has been assigned to Snail Bed {snail_bed.bed_name}.')

    # Check if the "Delete Employee" button was clicked
    if request.method == 'POST' and 'delete_employee' in request.POST:

        delete_form = DeleteEmployeeForm(request.POST)
        if delete_form.is_valid():
            employee_to_delete = delete_form.cleaned_data['employee_to_delete']
            user_to_delete = employee_to_delete.user
            username = employee_to_delete.user.username

            # Check if the employee is assigned to any snail bed before deletion
            if SnailBed.objects.filter(employee=employee_to_delete).exists():
                messages.error(request, f'Employee {username} is assigned to one or more Snail Beds. Unassign them first before deleting.')
            else:
                employee_to_delete.delete()
                user_to_delete.delete()
                messages.success(request, f'Employee {username} has been deleted.')

    else:
        delete_form = DeleteEmployeeForm()


    snail_beds = SnailBed.objects.filter(user=current_user)
    employees = EmployeeUser.objects.all()

    context = {
        'snail_beds': snail_beds,
        'employees': employees,
        'form': form,
        'delete_form': delete_form,
        }


    return render(request, 'admin_panel.html', context)

@login_required(login_url='login')
def manage_employee(request, employee_id):
    employee = get_object_or_404(EmployeeUser, pk=employee_id)
    snailbeds_assigned = SnailBed.objects.filter(employee=employee)

    if request.method == 'POST':
        form = EmployeeUserForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            # You can add a success message if needed
            # Redirect back to the manage_employee page
            return redirect('manage_employee', employee_id=employee.id)

        # Handle unassigning SnailBeds
        snailbed_id = request.POST.get('snailbed_id')
        if snailbed_id:
            snailbed_to_unassign = get_object_or_404(SnailBed, pk=snailbed_id)
            snailbed_to_unassign.employee = None
            snailbed_to_unassign.save()


        change_form = EmployeeChangeForm(request.POST, instance=employee)
        if change_form.is_valid():
            change_form.save()

            # Check if a new password is provided
            new_password = form.cleaned_data.get('new_password1')
            if new_password:
                employee.set_password(new_password)
                employee.save()
                update_session_auth_hash(request, employee)  # Keep the user logged in

            messages.success(request, 'Employee information updated successfully.')
            return redirect('manage_employee', employee_id=employee.id)


            messages.success(request, 'Employee information updated successfully.')
            return redirect('manage_employee', employee_id=employee.id)

            

    else:
        form = EmployeeUserForm(instance=employee)
        change_form = EmployeeChangeForm(instance=employee)

    context = {
        'employee': employee,
        'snailbeds_assigned': snailbeds_assigned,
        'form': form,
        'change_form': change_form,
    }
    return render(request, 'manage_employee.html', context)

class EmployeeUserListView(ListView):
    model = EmployeeUser
    template_name = 'employee_user_list.html'  # Create this template
    context_object_name = 'employees'  # Context variable name for the list of employees
    ordering = ['user__username']  # Define your desired ordering
    paginate_by = 10  # Set the number of items per page (adjust as needed)

@login_required(login_url='login')
def unassign_employee(request, snail_bed_id):

    current_user = AdminUser.objects.filter(user=request.user).first()
    if isinstance(current_user, AdminUser):
        snail_bed_to_unassign = get_object_or_404(SnailBed, pk=snail_bed_id)
        
        # Check if there is an employee assigned to the selected snail bed
        if snail_bed_to_unassign.employee:
            employee_to_unassign = snail_bed_to_unassign.employee
            snail_bed_to_unassign.employee = None
            snail_bed_to_unassign.save()
            messages.success(request, f'Employee {employee_to_unassign.user.username} has been unassigned from Snail Bed {snail_bed_to_unassign.bed_name}.')
        else:
            messages.error(request, f'There is no employee assigned to Snail Bed {snail_bed_to_unassign.bed_name}.')

    # Redirect back to the referring page or a default URL if 'HTTP_REFERER' is not available
    return redirect(request.META.get('HTTP_REFERER', reverse('dashboard')))

def log_snail_feed(request, snail_bed_id):
    snail_bed = get_object_or_404(SnailBed, id=snail_bed_id)
    if request.method == 'POST':
        form = SnailFeedForm(request.POST)
        if form.is_valid():
            form.instance.snail_bed = snail_bed
            form.save()
            # Redirect to a success page or back to the dashboard
            return redirect('dashboard')
    else:
        form = SnailFeedForm()
    return render(request, 'form_template.html', {'form': form, 'snail_bed': snail_bed})

def log_hatch_rate(request, snail_bed_id):
    snail_bed = get_object_or_404(SnailBed, id=snail_bed_id)
    
    if request.method == 'POST':
        form = SnailHatchRateForm(request.POST)
        if form.is_valid():
            form.instance.snail_bed = snail_bed
            form.save()
            # Redirect to a success page or back to the dashboard
            return redirect('dashboard')
    else:
        form = SnailHatchRateForm()
    
    return render(request, 'form_template.html', {'form': form, 'snail_bed': snail_bed})

def log_mortality_rate(request, snail_bed_id):
    snail_bed = get_object_or_404(SnailBed, id=snail_bed_id)
    
    if request.method == 'POST':
        form = SnailMortalityRateForm(request.POST)
        if form.is_valid():
            form.instance.snail_bed = snail_bed
            form.save()
            # Redirect to a success page or back to the dashboard
            return redirect('dashboard')
    else:
        form = SnailMortalityRateForm()
    
    return render(request, 'form_template.html', {'form': form, 'snail_bed': snail_bed})

def log_maturity_rate(request, snail_bed_id):
    snail_bed = get_object_or_404(SnailBed, id=snail_bed_id)
    
    if request.method == 'POST':
        form = TimeTakenToMatureForm(request.POST)
        if form.is_valid():
            form.instance.snail_bed = snail_bed
            form.save()
            # Redirect to a success page or back to the dashboard
            return redirect('dashboard')
    else:
        form = TimeTakenToMatureForm()
    
    return render(request, 'form_template.html', {'form': form, 'snail_bed': snail_bed})

@login_required(login_url='login')
def bed_performance(request, snail_bed_id):
    snail_bed = get_object_or_404(SnailBed, pk=snail_bed_id)

    # Retrieve the combined data
    snail_feeds = SnailFeed.objects.filter(snail_bed=snail_bed).order_by('consumed_on')
    hatch_rates = SnailHatchRate.objects.filter(snail_bed=snail_bed).order_by('datetime')
    mortality_rates = SnailMortalityRate.objects.filter(snail_bed=snail_bed).order_by('datetime')
    maturity_rates = TimeTakenToMature.objects.filter(snail_bed=snail_bed).order_by('snail_matured')

    # Check if there are enough data points for correlation calculation
    if len(snail_feeds) < 3 or len(hatch_rates) < 3 or len(mortality_rates) < 3 or len(maturity_rates) < 3:
        messages.error(request, "There is not enough for performance estimation. Snail Bed should have at least 3 logs for each data field.")
        return redirect('dashboard')  # Redirect to a suitable page

    # Calculate the average hatch rate
    summed_hatch_rates = 0
    iteration_counter = 0
    hatch_rates_for_snail_bed = SnailHatchRate.objects.filter(snail_bed=snail_bed)
    if len(hatch_rates_for_snail_bed) > 0:
        for hatch_rate in hatch_rates_for_snail_bed:
            if hatch_rate.hatch_rate_percentage is not 0: # dont count initial snail population of bed which results in 0 rate
                summed_hatch_rates += hatch_rate.hatch_rate_percentage
                iteration_counter += 1
        # in case that there was a record but it was 0, counter will remain zero and division by zero will occurr as error
        if iteration_counter is 0:
            iteration_counter = 1
        average_hatch_rate_for_snail_bed = summed_hatch_rates / iteration_counter
    else:
        average_hatch_rate_for_snail_bed = 0


    # Calculate the average mortality rate
    summed_mortality_rates = 0
    iteration_counter = 0
    mortality_rates_for_snail_bed = SnailMortalityRate.objects.filter(snail_bed=snail_bed)
    if len(mortality_rates_for_snail_bed) > 0:
        for mortality_rate in mortality_rates_for_snail_bed:
            if mortality_rate.mortality_rate_percentage is not 0: # dont count initial snail population of bed which results in 0 rate
                summed_mortality_rates += mortality_rate.mortality_rate_percentage
                iteration_counter += 1
        # in case that there was a record but it was 0, counter will remain zero and division by zero will occurr as error
        if iteration_counter is 0:
            iteration_counter = 1
        average_mortality_rate_for_snail_bed = summed_mortality_rates / iteration_counter
    else:
        average_mortality_rate_for_snail_bed = 0



    # Calculate the average maturity rate and average days to mature
    summed_maturity_rates = 0
    summed_days_to_mature = 0
    iteration_counter = 0
    maturity_rates_for_snail_bed = TimeTakenToMature.objects.filter(snail_bed=snail_bed)
    if len(maturity_rates_for_snail_bed) > 0:
        for maturity_rate in maturity_rates_for_snail_bed:
            if maturity_rate.maturity_percentage is not None: # dont count initial snail population of bed which results in 0 rate
                summed_maturity_rates += maturity_rate.maturity_percentage
            if maturity_rate.days_to_mature is not None and maturity_rate.days_to_mature > 0:
                summed_days_to_mature += maturity_rate.days_to_mature
            iteration_counter += 1
        # in case that there was a record but it was 0, counter will remain zero and division by zero will occurr as error
        if iteration_counter is 0:
            iteration_counter = 1
        average_maturity_rate_for_snail_bed = summed_maturity_rates / iteration_counter
        average_days_to_mature_for_snail_bed = summed_days_to_mature / iteration_counter
    else:
        average_maturity_rate_for_snail_bed = 0
        average_days_to_mature_for_snail_bed = 0

   
    # Get the existing SnailBedPerformance object related to this SnailBed
    bed_performance, created = SnailBedPerformance.objects.get_or_create(snail_bed=snail_bed)

    # Update the fields with the calculated averages
    bed_performance.average_hatch_rate = average_hatch_rate_for_snail_bed
    bed_performance.average_mortality_rate = average_mortality_rate_for_snail_bed 
    bed_performance.average_maturity_rate = average_maturity_rate_for_snail_bed
    bed_performance.actual_average_time_to_maturity = average_days_to_mature_for_snail_bed
    bed_performance.save()


    if request.method == 'POST' and 'forecast_hatch' in request.POST:
        # Get the existing SnailBedPerformance object related to this SnailBed
        # if there is a forecast use that, or create new one
        forecast_hatch, created = ForecastedHatchRate.objects.get_or_create(snail_bed=snail_bed)
    else:
        # Check if a forecast exists for the SnailBed
        forecast_hatch = ForecastedHatchRate.objects.filter(snail_bed=snail_bed).first()

    if request.method == 'POST' and 'forecast_mortality' in request.POST:
        forecast_mortality, created = ForecastedMortalityRate.objects.get_or_create(snail_bed=snail_bed)
    else:
        forecast_mortality = ForecastedMortalityRate.objects.filter(snail_bed=snail_bed).first()

    if request.method == 'POST' and 'forecast_maturity' in request.POST:
        forecast_maturity, created = ForecastedMaturityRate.objects.get_or_create(snail_bed=snail_bed)
    else:
        forecast_maturity = ForecastedMaturityRate.objects.filter(snail_bed=snail_bed).first()

    context = {
        'bed_performance': bed_performance,
        'forecast_hatch': None,
        'html_table_hatch': None,
        'forecast_mortality': None,
        'html_table_mortality': None,
        'forecast_maturity': None,
        'html_table_maturity': None,
    }

    if forecast_hatch:
        html_table_hatch = forecast_hatch.forecasted_value_pyaf.to_html() # Convert DataFrame to HTML
        context['forecast_hatch'] = forecast_hatch
        context['html_table_hatch'] = html_table_hatch

    if forecast_mortality:
        html_table_mortality = forecast_mortality.forecasted_value_pyaf.to_html() # Convert DataFrame to HTML
        context['forecast_mortality'] = forecast_mortality
        context['html_table_mortality'] = html_table_mortality

    if forecast_maturity:
        html_table_maturity = forecast_maturity.forecasted_value_pyaf.to_html()
        context['forecast_maturity'] = forecast_maturity
        context['html_table_maturity'] = html_table_maturity

    return render(request, 'bed_performance.html', context)

@login_required(login_url='login')
def delete_snailbed(request, snail_bed_id):
    # Fetch the SnailBed object to be deleted
    snail_bed_to_delete = get_object_or_404(SnailBed, id=snail_bed_id)
    current_user = AdminUser.objects.filter(user=request.user).first()
    # Check if the user has the permission to delete this snail bed
    if isinstance(current_user, AdminUser):
        # Delete the SnailBed object and let user know it's done
        messages.success(request, f"You have successfully deleted: {snail_bed_to_delete.bed_name}")
        snail_bed_to_delete.delete()
        # Redirect to the dashboard or another appropriate page
        return redirect('dashboard')
    else:
        # If the user doesn't have permission, you can show an error message or handle it as needed
        messages.error(request, "You must be an Admin user to delete a Snail Bed.")
        return redirect('dashboard')  # Redirect to a suitable page

class SnailHatchRateListView(ListView):
    model = SnailHatchRate
    template_name = 'history.html'
    context_object_name = 'history_data'

    def get_queryset(self):
        snail_bed = get_object_or_404(SnailBed, id=self.kwargs['snail_bed_id'])
        return SnailHatchRate.objects.filter(snail_bed=snail_bed).order_by('-datetime')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['snail_bed'] = get_object_or_404(SnailBed, id=self.kwargs['snail_bed_id'])
        return context

class SnailMortalityRateListView(ListView):
    model = SnailMortalityRate
    template_name = 'history.html'
    context_object_name = 'history_data'

    def get_queryset(self):
        snail_bed = get_object_or_404(SnailBed, id=self.kwargs['snail_bed_id'])
        return SnailMortalityRate.objects.filter(snail_bed=snail_bed).order_by('-datetime')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['snail_bed'] = get_object_or_404(SnailBed, id=self.kwargs['snail_bed_id'])
        return context

class SnailFeedListView(ListView):
    model = SnailFeed
    template_name = 'history.html'
    context_object_name = 'history_data'

    def get_queryset(self):
        snail_bed = get_object_or_404(SnailBed, id=self.kwargs['snail_bed_id'])
        return SnailFeed.objects.filter(snail_bed=snail_bed).order_by('-consumed_on')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['snail_bed'] = get_object_or_404(SnailBed, id=self.kwargs['snail_bed_id'])
        return context

class TimeTakenToMatureListView(ListView):
    model = TimeTakenToMature
    template_name = 'history.html'
    context_object_name = 'history_data'

    def get_queryset(self):
        snail_bed = get_object_or_404(SnailBed, id=self.kwargs['snail_bed_id'])
        return TimeTakenToMature.objects.filter(snail_bed=snail_bed).order_by('-snail_matured')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['snail_bed'] = get_object_or_404(SnailBed, id=self.kwargs['snail_bed_id'])
        return context


@login_required
def create_snailbeds(request):
    # Get the logged-in user's AdminUser object
    current_user = AdminUser.objects.filter(user=request.user).first()
    current_time = timezone.now()

    # Create a list to store SnailBed instances
    snail_beds = []

    # Create SnailBed instances
    for j in range(1):
        bed_name = f'Snail Bed #{j}'

        # Ensure bed_name is unique
        while SnailBed.objects.filter(bed_name=bed_name).exists():
            j += 1
            bed_name = f'Snail Bed #{j}'
        
        snail_bed = SnailBed.objects.create(bed_name=bed_name, user=current_user)
        snail_beds.append(snail_bed)

        # Create SnailHatchRate instances
        for i in range(30):
            SnailHatchRate.objects.create(
                snail_bed=snail_bed,
                newly_hatched_snails=random.randint(200, 1200), # hatch rate should in theory be much larger than mortality
                datetime=current_time + timedelta(weeks=i),# increment to occur each week
            )

        # Create SnailMortalityRate instances
        for i in range(30):
            if snail_bed.snail_amount <= 0:
                SnailMortalityRate.objects.create(
                    snail_bed=snail_bed,
                    expired_snail_amount=0,
                    datetime=current_time + timedelta(weeks=i),# increment to occur each week
                )
            else:
                SnailMortalityRate.objects.create(
                    snail_bed=snail_bed,
                    expired_snail_amount=random.randint(100, 1000),
                    datetime=current_time + timedelta(weeks=i),
                )

        # Create SnailFeed instances
        for i in range(30):
            SnailFeed.objects.create(
                snail_bed=snail_bed,
                consumed_on=current_time + timedelta(weeks=i), # increment to occur each week
                grams_feed_given=random.randint(100, 1000)
            )

        # Create TimeTakenToMature instances
        for i in range(30):
            days_to_mature = random.randint(20, 40)
            snails_matured_count = random.randint(100, 1000)
            snail_hatched = current_time + timedelta(weeks=i) # increment to occur each week
            snail_matured = snail_hatched + timedelta(days=days_to_mature) # should occur 20-40 days after hatch
            TimeTakenToMature.objects.create(
                snail_bed=snail_bed,
                snail_hatched=snail_hatched,
                snail_matured=snail_matured,
                snails_matured_count=snails_matured_count,
            )

    messages.success(request, "We've successfully created Snail Bed dummy data and added it to your dashboard!")
    return HttpResponseRedirect(reverse('dashboard'))

