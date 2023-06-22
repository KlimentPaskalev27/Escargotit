from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from django.views.decorators.csrf import csrf_exempt #cross-site validation certificate exemption classes from django
from .models import *
#from .serialisers import *