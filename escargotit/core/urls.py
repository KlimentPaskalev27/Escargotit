from django.urls import path
from . import views
from . import api
from .views import *


urlpatterns = [

     # Homepage
    path('', views.IndexCreateView.as_view(), name='home'),

    # Terms and Conditions
    #path('terms/', views.terms_and_conditions, name='terms'),

    # Snail Bed Form
    #path('snailbed/new/', views.create_snail_bed, name='create_snail_bed'),

    # Inventory Panel Form
    #path('inventory/panel/new/', views.create_inventory_panel, name='create_inventory_panel'),

    # User Registration Form
    #path('register/', views.register, name='register'),

    # Login Form
    #path('login/', views.login, name='login'),

    # API Data Export
    #path('api/data/export/', views.api_data_export, name='api-data-export'),


    # URLs for forms
    # path('create_snail_bed/', views.create_snail_bed, name='create_snail_bed'),
    # path('create_feed/', views.create_feed, name='create_feed'),
    # path('create_medicine/', views.create_medicine, name='create_medicine'),
    # path('create_staff_usable_item/', views.create_staff_usable_item, name='create_staff_usable_item'),
    # path('create_cleaning_product/', views.create_cleaning_product, name='create_cleaning_product'),
    # path('create_snail_performance/', views.create_snail_performance, name='create_snail_performance'),

    # # URLs for dashboards and panels
    # path('inventory_panel/', views.inventory_panel, name='inventory_panel'),
    # path('snail_bed_dashboard/<int:snail_bed_id>/', views.snail_bed_dashboard, name='snail_bed_dashboard'),
    # path('feed_dashboard/<int:feed_id>/', views.feed_dashboard, name='feed_dashboard'),
    # path('medicine_dashboard/<int:medicine_id>/', views.medicine_dashboard, name='medicine_dashboard'),
    # path('staff_usable_item_dashboard/<int:staff_usable_item_id>/', views.staff_usable_item_dashboard, name='staff_usable_item_dashboard'),
    # path('cleaning_product_dashboard/<int:cleaning_product_id>/', views.cleaning_product_dashboard, name='cleaning_product_dashboard'),
    # path('snail_performance_dashboard/<int:snail_performance_id>/', views.snail_performance_dashboard, name='snail_performance_dashboard'),


    #  # API endpoints for SnailBed class
    # path('api/snailbed/', views.SnailBedListCreateAPIView.as_view(), name='snailbed-list-create'),
    # path('api/snailbed/<int:pk>/', views.SnailBedRetrieveUpdateDestroyAPIView.as_view(), name='snailbed-retrieve-update-destroy'),

    # # API endpoints for Feed class
    # path('api/feed/', views.FeedListCreateAPIView.as_view(), name='feed-list-create'),
    # path('api/feed/<int:pk>/', views.FeedRetrieveUpdateDestroyAPIView.as_view(), name='feed-retrieve-update-destroy'),

    # # API endpoints for Medicine class
    # path('api/medicine/', views.MedicineListCreateAPIView.as_view(), name='medicine-list-create'),
    # path('api/medicine/<int:pk>/', views.MedicineRetrieveUpdateDestroyAPIView.as_view(), name='medicine-retrieve-update-destroy'),

    # # API endpoints for StaffUsableItems class
    # path('api/staffusableitems/', views.StaffUsableItemsListCreateAPIView.as_view(), name='staffusableitems-list-create'),
    # path('api/staffusableitems/<int:pk>/', views.StaffUsableItemsRetrieveUpdateDestroyAPIView.as_view(), name='staffusableitems-retrieve-update-destroy'),

    # # API endpoints for CleaningProducts class
    # path('api/cleaningproducts/', views.CleaningProductsListCreateAPIView.as_view(), name='cleaningproducts-list-create'),
    # path('api/cleaningproducts/<int:pk>/', views.CleaningProductsRetrieveUpdateDestroyAPIView.as_view(), name='cleaningproducts-retrieve-update-destroy'),

    # # API endpoints for SnailPerformance class
    # path('api/snailperformance/', views.SnailPerformanceListCreateAPIView.as_view(), name='snailperformance-list-create'),
    # path('api/snailperformance/<int:pk>/', views.SnailPerformanceRetrieveUpdateDestroyAPIView.as_view(), name='snailperformance-retrieve-update-destroy'),
]