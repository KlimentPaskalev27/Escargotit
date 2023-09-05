from django.shortcuts import render, redirect, HttpResponse
from .forms import *
from .models import *
from django.contrib.auth.models import User 
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponseRedirect

def index(request):
    first_snail_performance = SnailPerformance.objects.first()
    forecasts = ForecastedBirthRate.objects.first()

    a = first_snail_performance

    # Convert DataFrame to HTML
    html_table = forecasts.forecasted_value_pyaf.to_html()

    context = {
        'snail_performance': a,
        'forecasts': forecasts,
        'html_table': html_table,
    }

    return render(request, 'index.html', context)


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
        snail_birth_rate_form = SnailBirthRateForm()
        snail_mortality_rate_form = SnailMortalityRateForm()
        time_taken_to_mature_form = TimeTakenToMatureForm()
        snail_performance_form = SnailPerformanceForm()

    return render(request, 'snail_data_form.html', {
        'snail_feed_form': snail_feed_form,
        'snail_birth_rate_form': snail_birth_rate_form,
        'snail_mortality_rate_form': snail_mortality_rate_form,
        'time_taken_to_mature_form': time_taken_to_mature_form,
        'snail_performance_form': snail_performance_form,
    
    })



@login_required
def dashboard(request):
    # Handle the POST request to add a new SnailBed object
    if request.method == 'POST':
        # Create a new SnailBed object based on the form data
        new_snail_bed = SnailBed(
            bed_name=request.POST.get('bed_name', "name"),
            user=request.user,
            location=request.POST.get('location', ''), 
        )
        new_snail_bed.save()  # Save the new SnailBed to the database

        # After processing the POST request, redirect to the dashboard page using the GET method
        return HttpResponseRedirect(request.path_info)  # Redirect to the same page (GET request)

    # Retrieve all SnailBeds for the logged-in user
    snail_beds = SnailBed.objects.filter(user=request.user)
    snail_bed_count = snail_beds.count()

    return render(request, 'dashboard.html', {'snail_beds': snail_beds, 'snail_bed_count': snail_bed_count})


def delete_all_snailbeds(request):
    # Assuming you have a user-based association in your SnailBed model
    # You should adjust this logic based on your model structure
    SnailBed.objects.filter(user=request.user).delete()
    return redirect('dashboard')  # Redirect back to the dashboard 

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect to the dashboard view after successful login
        else:
            # Handle invalid login credentials, display an error message, etc.
            pass  # You can add your custom error handling here

    return render(request, 'registration/login.html')  # Render the login page template


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

