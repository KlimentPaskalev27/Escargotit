from rest_framework import serializers
from .models import *

class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminUser
        fields = '__all__'

class EmployeeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeUser
        fields = '__all__'

class SnailBedSerializer(serializers.ModelSerializer):
    class Meta:
        model = SnailBed
        fields = '__all__'