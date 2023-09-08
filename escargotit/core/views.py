from django.shortcuts import render, redirect, HttpResponse
from .forms import *
from .models import *
from django.contrib.auth.models import User 
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponseRedirect

from django.views.generic import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView



import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from scipy.stats import pearsonr  # For calculating correlation coefficient
# https://scipy.org/install/




from .faq_data import faq_data  # Import the faq_data from the module

@login_required
def performance(request):
    first_snail_bed_performance = SnailBedPerformance.objects.first()
    forecasts = ForecastedHatchRate.objects.first()

    a = first_snail_bed_performance

    # Convert DataFrame to HTML
    html_table = forecasts.forecasted_value_pyaf.to_html()

    context = {
        'snail_bed_performance': a,
        'forecasts': forecasts,
        'html_table': html_table,
    }

    return render(request, 'performance.html', context)


@login_required
def snail_data_form(request):
    if request.method == 'POST':
        form = SnailDataForm(request.POST)
        if form.is_valid():
            # Process and save the form data to the appropriate models
            form.save()
            return redirect('success_page')  # Redirect to a success page
    else:
        # Create forms for all models
        snail_feed_form = SnailFeedForm()
        snail_hatch_rate_form = SnailHatchRateForm()
        snail_mortality_rate_form = SnailMortalityRateForm()
        time_taken_to_mature_form = TimeTakenToMatureForm()
        snail_bed_performance_form = SnailBedPerformanceForm()

    return render(request, 'snail_data_form.html', {
        'snail_feed_form': snail_feed_form,
        'snail_hatch_rate_form': snail_hatch_rate_form,
        'snail_mortality_rate_form': snail_mortality_rate_form,
        'time_taken_to_mature_form': time_taken_to_mature_form,
        'snail_bed_performance_form': snail_bed_performance_form,
    
    })



@login_required
def dashboard(request):

    current_user = AdminUser.objects.filter(user=request.user).first()
    
    # Handle the POST request to add a new SnailBed object
    if request.method == 'POST':
        # Create a new SnailBed object based on the form data
        new_snail_bed = SnailBed(
            #bed_name=request.POST.get('bed_name', ""),
            #bed_name="",
            user=current_user,
            #snail_amount=0,
            #hatch_rate="",
            #mortality_rate="",
        )
        new_snail_bed.save()  # Save the new SnailBed to the database

        # After processing the POST request, redirect to the dashboard page using the GET method
        return HttpResponseRedirect(request.path_info)  # Redirect to the same page (GET request)

    # Retrieve all SnailBeds for the logged-in user
    snail_beds = SnailBed.objects.filter(user=current_user)
    snail_bed_count = snail_beds.count()

    return render(request, 'dashboard.html', {'snail_beds': snail_beds, 'snail_bed_count': snail_bed_count})

@login_required
def index(request):

    current_user = AdminUser.objects.filter(user=request.user).first()

    # Handle the POST request to add a new SnailBed object
    if request.method == 'POST':
        
        # Create a new SnailBed object based on the form data
        new_snail_bed = SnailBed.objects.create(
            user = current_user,
        )
        new_snail_bed.save()  # Save the new SnailBed to the database

        # After processing the POST request, redirect to the dashboard page using the GET method
        return HttpResponseRedirect(request.path_info)  # Redirect to the same page (GET request)

    # Retrieve all SnailBeds for the logged-in user
    snail_beds = SnailBed.objects.filter(user=current_user)
    snail_bed_count = snail_beds.count()

    return render(request, 'dashboard.html', {'snail_beds': snail_beds, 'snail_bed_count': snail_bed_count})


def delete_all_snailbeds(request):
    # Assuming you have a user-based association in your SnailBed model
    # You should adjust this logic based on your model structure
    SnailBed.objects.filter(user=request.user).delete()
    return redirect('dashboard')  # Redirect back to the dashboard 



from django.contrib import messages  # Import the messages module

class RegisterFormView(SuccessMessageMixin, CreateView):
    form_class = RegisterForm #CustomUserCreationForm  # Use the CustomUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')  # Use reverse_lazy to specify the URL for the login page
    success_message = "Your profile was created successfully"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response


class LoginFormView(LoginView):
    template_name = 'registration/login.html'
    success_url = ' '


@login_required
def logout_view(request):
    logout(request)
    # Redirect to a logout success page or login page
    return redirect('login')


@login_required
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




from scipy.stats import pearsonr  # Import Pearson correlation coefficient
def barchart_with_correlation(request):
    # Retrieve the combined data
    snail_feeds = SnailFeed.objects.all().order_by('consumed_on')
    hatch_rates = SnailHatchRate.objects.all().order_by('datetime')

    # Extract grams feed given and hatch rates
    grams_feed_given = [entry.grams_feed_given for entry in snail_feeds]
    hatch_rates_percentage = [entry.hatch_rate_percentage for entry in hatch_rates]

    # Calculate percentage change for grams feed given
    grams_feed_change = [0]  # Initial value is 0
    for i in range(1, len(grams_feed_given)):
        percentage_change = ((grams_feed_given[i] - grams_feed_given[i - 1]) / grams_feed_given[i - 1]) * 100
        grams_feed_change.append(percentage_change)

    # Calculate percentage change for hatch rates
    hatch_rate_change = [0]  # Initial value is 0
    for i in range(1, len(hatch_rates_percentage)):
        percentage_change = ((hatch_rates_percentage[i] - hatch_rates_percentage[i - 1]) / hatch_rates_percentage[i - 1]) * 100
        hatch_rate_change.append(percentage_change)

    # Ensure both arrays have the same length (truncate the longer one)
    min_length = min(len(grams_feed_change), len(hatch_rate_change))
    grams_feed_change = grams_feed_change[:min_length]
    hatch_rate_change = hatch_rate_change[:min_length]

    # Calculate the Pearson correlation coefficient
    correlation_coefficient, _ = pearsonr(grams_feed_change, hatch_rate_change)

    # Create the overlapping bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(np.arange(min_length), grams_feed_change, alpha=0.5, label='Grams Feed Change (%)', width=0.4)
    plt.bar(np.arange(min_length), hatch_rate_change, alpha=0.5, label='Hatch Rate Change (%)', width=0.4)
    plt.xlabel('Date')
    plt.ylabel('Percentage Change (%)')
    plt.title(f'Overlapping Bar Chart of Percentage Change (Correlation: {correlation_coefficient:.2f})')  # Display correlation
    plt.xticks(np.arange(min_length), snail_feeds.values_list('consumed_on', flat=True)[:min_length], rotation=45)
    plt.legend()

    # Save the plot to a BytesIO object
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    # Convert the plot to base64 for embedding in HTML
    plot_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    context = {
        'plot_base64': plot_base64,
    }

    return render(request, 'barchart.html', context)


def barchart(request):
    # Retrieve the combined data
    snail_feeds = SnailFeed.objects.all().order_by('consumed_on')
    hatch_rates = SnailHatchRate.objects.all().order_by('datetime')

    # Extract grams feed given and hatch rates
    grams_feed_given = [entry.grams_feed_given for entry in snail_feeds]
    hatch_rates_percentage = [entry.hatch_rate_percentage for entry in hatch_rates]

    # Calculate percentage change for grams feed given
    grams_feed_change = [0]  # Initial value is 0
    for i in range(1, len(grams_feed_given)):
        percentage_change = ((grams_feed_given[i] - grams_feed_given[i - 1]) / grams_feed_given[i - 1]) * 100
        grams_feed_change.append(percentage_change)

    # Calculate percentage change for hatch rates
    hatch_rate_change = [0]  # Initial value is 0
    for i in range(1, len(hatch_rates_percentage)):
        percentage_change = ((hatch_rates_percentage[i] - hatch_rates_percentage[i - 1]) / hatch_rates_percentage[i - 1]) * 100
        hatch_rate_change.append(percentage_change)

    # Create the overlapping bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(snail_feeds.values_list('consumed_on', flat=True), grams_feed_change, alpha=0.5, label='Grams Feed Change (%)', width=0.4)
    plt.bar(hatch_rates.values_list('datetime', flat=True), hatch_rate_change, alpha=0.5, label='Hatch Rate Change (%)', width=0.4)
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
        'plot_base64': plot_base64,
    }

    return render(request, 'barchart.html', context)




from django.shortcuts import get_object_or_404



def custom_admin_panel(request):

    current_user = AdminUser.objects.filter(user=request.user).first()

    if request.method == 'POST':
        form = EmployeeCreationForm(request.POST)
        #form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Employee user {username} has been created.')
            return redirect('custom_admin_panel')
    else:
        form = UserCreationForm()

    snail_beds = SnailBed.objects.filter(user=current_user)
    employees = EmployeeUser.objects.all()

     # Add code to handle the assignment of existing employees to snail beds
    if request.method == 'POST' and 'assign_employee' in request.POST:
        snail_bed_id = request.POST.get('snail_bed_id')
        employee_id = request.POST.get('employee_id')
        snail_bed = get_object_or_404(SnailBed, pk=snail_bed_id)
        employee = get_object_or_404(EmployeeUser, pk=employee_id)
        snail_bed.employees = employee
        snail_bed.save()
        messages.success(request, f'Employee {employee.user.username} has been assigned to Snail Bed {snail_bed.bed_name}.')

    context = {
        'snail_beds': snail_beds,
        'employees': employees,
        'form': form
        }

    return render(request, 'admin_panel.html', context)