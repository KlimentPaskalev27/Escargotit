from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from .views import *

from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()


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

    # User Settings
    path('user/settings/', views.user_settings, name='user_settings'),



    # Include the API endpoints
    path('api/', include(router.urls)),

    path('delete_all_snailbeds/', views.delete_all_snailbeds, name='delete_all_snailbeds'),


    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),

    path('terms/', views.terms, name='terms'),
    path('cookies/', views.cookies, name='cookies'),
    path('privacy/', views.privacy, name='privacy'),
    path('faqs/', views.faqs, name='faqs'),

    path('barchart/', views.barchart, name='barchart'),
    path('barchart-with-correlation/', views.barchart_with_correlation, name='barchart_with_correlation'),


]