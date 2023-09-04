from django.urls import path
from . import views

from .views import *


urlpatterns = [
    # Site structure urls
    path('', views.index, name='index'),

    path('snail-data-form/', views.snail_data_form, name='snail_data_form'),

    path('dashboard/', views.dashboard, name='dashboard'),
]