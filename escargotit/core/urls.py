from django.urls import path
from . import views

from .views import *


urlpatterns = [
    # Site structure urls
    path('', views.index, name='index'),
]