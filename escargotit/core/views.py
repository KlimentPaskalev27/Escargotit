
from django.shortcuts import render, redirect

from .models import *


def index(request):
    first_snail_performance = SnailPerformance.objects.first()
    forecasts = ForecastedBirthRate.objects.first()

    a = first_snail_performance
    
    # if a.snail_feed <= 0 or not a.snail_feed:
    #     a.snail_feed = 0
    # if a.snail_birth_rate <= 0 or not a.snail_birth_rate:
    #     a.snail_birth_rate = 0
    # if a.snail_mortality_rate <= 0 or not a.snail_mortality_rate:
    #     a.snail_mortality_rate = 0
    # if a.time_taken_to_mature <= 0 or not a.time_taken_to_mature:
    #     a.time_taken_to_mature = 0
    # if a.bed_performance <= 0 or not a.bed_performance:
    #     a.bed_performance = 0

    # Convert DataFrame to HTML
    html_table = forecasts.forecasted_value_pyaf.to_html()

    context = {
        'snail_performance': a,
        'forecasts': forecasts,
        'html_table': html_table,
    }

        

    return render(request, 'index.html', context)
