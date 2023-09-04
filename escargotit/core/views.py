
from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib.auth.models import User 


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


