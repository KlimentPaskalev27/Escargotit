# myapp/serializers.py

from rest_framework import serializers
from .models import SnailBed

class SnailBedSerializer(serializers.ModelSerializer):
    class Meta:
        model = SnailBed
        fields = '__all__'
