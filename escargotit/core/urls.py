from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from .views import *

from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()


urlpatterns = [
    # Main Features
    path('performance/', views.performance, name='performance'),

    path('home/', views.home, name='home'),

    path('', views.index, name='index'),

    path('snail-data-form/', views.snail_data_form, name='snail_data_form'),

    path('dashboard/', views.dashboard, name='dashboard'),


    # Registration
    path('register/', views.RegisterFormView.as_view() , name='register'),

    # Login
    path('login', views.LoginFormView.as_view() , name='login'),

    # Logout
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),

    # User Settings
    path('user/settings/', views.user_settings, name='user_settings'),

    # API endpoints
    path('api/', include(router.urls)),

    path('delete_all_snailbeds/', views.delete_all_snailbeds, name='delete_all_snailbeds'),

    # Company pages
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('terms/', views.terms, name='terms'),
    path('cookies/', views.cookies, name='cookies'),
    path('privacy/', views.privacy, name='privacy'),
    path('faqs/', views.faqs, name='faqs'),

    # Statistics and Insights
    path('barchart/<int:snail_bed_id>/', views.barchart, name='barchart'),

    path('custom_admin_panel/', views.custom_admin_panel, name='custom_admin_panel'),


    path('unassign_employee/<int:snail_bed_id>/', views.unassign_employee, name='unassign_employee'),

    path('manage_employee/<int:employee_id>/', views.manage_employee, name='manage_employee'),

    path('employees/', EmployeeUserListView.as_view(), name='employees'),

    # URL for logging data options
    path('log-data/<int:snail_bed_id>/', views.log_data_options, name='log_data_options'),

    # URLs for specific data logging forms
    path('log_snail_feed/<int:snail_bed_id>/', views.log_snail_feed, name='log_snail_feed'),
    path('log_hatch_rate/<int:snail_bed_id>/', views.log_hatch_rate, name='log_hatch_rate'),
    path('log_mortality_rate/<int:snail_bed_id>/', views.log_mortality_rate, name='log_mortality_rate'),
    path('log_maturity_rate/<int:snail_bed_id>/', views.log_maturity_rate, name='log_maturity_rate'),

    path('bed_performance/<int:snail_bed_id>/', views.bed_performance, name='bed_performance'),

    path('view_hatch_rate_history/<int:snail_bed_id>/', views.SnailHatchRateListView.as_view(), name='view_hatch_rate_history'),
    path('view_mortality_rate_history/<int:snail_bed_id>/', views.SnailMortalityRateListView.as_view(), name='view_mortality_rate_history'),
    path('view_maturity_rate_history/<int:snail_bed_id>/', views.TimeTakenToMatureListView.as_view(), name='view_maturity_rate_history'),
    path('view_feed_history/<int:snail_bed_id>/', views.SnailFeedListView.as_view(), name='view_feed_history'),
]