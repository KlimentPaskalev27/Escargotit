from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import *


urlpatterns = [
    # Site structure urls
    path('', views.index, name='index'),

    path('snail-data-form/', views.snail_data_form, name='snail_data_form'),

    path('dashboard/', views.dashboard, name='dashboard'),


     # Registration
    path('register/', views.register, name='register'),

    # Login
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),

    # Logout
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
]