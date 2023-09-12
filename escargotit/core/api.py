from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *


class EmployeeUserViewSet(generics.ListAPIView):
    serializer_class = EmployeeUserSerializer

    def get_queryset(self):
        user = self.request.user
        admin = AdminUser.objects.filter(user=user).first()
        return EmployeeUser.objects.filter(admin=admin)

class SnailBedViewSet(generics.ListAPIView):
    serializer_class = SnailBedSerializer

    def get_queryset(self):
        user = self.request.user
        admin = AdminUser.objects.filter(user=user).first()
        return SnailBed.objects.filter(user=admin)