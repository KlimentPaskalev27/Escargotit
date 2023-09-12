from rest_framework import generics, viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
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

class SpecificSnailBedView(APIView):
    def get(self, request, snail_bed_id):
        user = self.request.user
        admin = AdminUser.objects.filter(user=user).first()

        try:
            # Retrieve the SnailBed object based on the provided ID
            snail_bed = SnailBed.objects.get(pk=snail_bed_id, user=admin)
            # Serialize the SnailBed data
            serializer = SpecificSnailBedSerializer(snail_bed)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        except SnailBed.DoesNotExist:
            return Response(
                {"detail": "SnailBed not found."},
                status=status.HTTP_404_NOT_FOUND
            )