from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
from rest_framework import generics


class AdminUserViewSet(generics.ListAPIView):
    queryset = AdminUser.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = [IsAuthenticated]

class EmployeeUserViewSet(generics.ListAPIView):
    queryset = EmployeeUser.objects.all()
    serializer_class = EmployeeUserSerializer

class SnailBedViewSet(generics.ListAPIView):
    queryset = SnailBed.objects.all()
    serializer_class = SnailBedSerializer