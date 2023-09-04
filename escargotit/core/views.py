
from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib.auth.models import User 
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm


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



# def snail_data_form(request):
#     if request.method == 'POST':
#         form = SnailDataForm(request.POST)
#         if form.is_valid():
#             # Process and save the form data to the appropriate models
#             form.save()
#             return redirect('success_page')  # Redirect to a success page
#     else:
#         form = SnailDataForm()

#     return render(request, 'snail_data_form.html', {'form': form})


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


def dashboard(request):
    # Replace 'dummy_user' with the user you want to display
    # dummy_user = User.objects.get(username='dummy_user')
    # dummy_user = {
    #     profile: {
    #         username: "kliment",
    #         first_name: "kliment",
    #         last_name: "paskalev",
    #         email: "kliment@email.com",

    #     },
    # }

    # define a class
    class User:
        username= "kliment"
        first_name= "kliment"
        last_name="paskalev"
        email="kliment@email.com"

    # dummy_user1 = {
    #     username: "kliment",
    #     first_name: "kliment",
    #     last_name: "paskalev",
    #     email: "kliment@email.com",
    # }

    dummy_user2 = User()

   
    context = {'user_profile': dummy_user2}  # Replace '.profile' with your user profile attribute
    return render(request, 'dashboard.html', context)


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        user = User.objects.create_user(username=username, password=password, email=email)
        login(request, user)  # Log the user in after registration
        # Redirect to a success page or dashboard
        return redirect('dashboard')
    return render(request, 'registration/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page or dashboard
            return redirect('dashboard')
        else:
            # Handle login failure (e.g., display an error message)
            return render(request, 'registration/login.html', {'error_message': 'Invalid login credentials'})
    return render(request, 'registration/login.html')


@login_required
def logout_view(request):
    logout(request)
    # Redirect to a logout success page or login page
    return redirect('login')


@login_required
def user_settings(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user_settings')  # Redirect after successful update
    else:
        form = UserChangeForm(instance=request.user)
    return render(request, 'registration/user_settings.html', {'form': form})
