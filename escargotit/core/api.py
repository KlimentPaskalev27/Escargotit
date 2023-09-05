# myapp/api.py

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import SnailBed
from .serializers import SnailBedSerializer

class SnailBedViewSet(viewsets.ModelViewSet):
    queryset = SnailBed.objects.all()
    serializer_class = SnailBedSerializer
    permission_classes = [IsAuthenticated]

