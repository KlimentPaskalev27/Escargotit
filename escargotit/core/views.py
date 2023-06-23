
from django.shortcuts import render, redirect

from .models import *


def index(request):
    first_snail_performance = SnailPerformance.objects.first()

    context = {
        'snail_performance': first_snail_performance,
    }

    return render(request, 'index.html', context)
