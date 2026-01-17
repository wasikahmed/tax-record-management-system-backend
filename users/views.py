from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from .permissions import IsTaxOfficer, IsOwnerOrOfficer, IsTaxPayer
from .models import TaxPayerProfile, TaxZone, TaxCategory, TaxOfficerProfile
from .serializers import (
    TaxPayerProfileSerializer,
    TaxZoneSerializer,
    TaxCategorySerializer,
    TaxOfficerProfileSerializer,
    CustomTokenObtainPairSerializer,
)


class TaxZoneListCreateView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsTaxOfficer()]
        return [permissions.AllowAny()]

    def get(self, request):
        zones = TaxZone.objects.all()
        serializer = TaxZoneSerializer(zones, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = TaxZoneSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaxCategoryListCreateView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsTaxOfficer()]
        return [permissions.AllowAny()]

    def get(self, request):
        categories = TaxCategory.objects.all()
        serializer = TaxCategorySerializer(categories, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = TaxCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# TaxPayer Views

class TaxPayerListCreateView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [AllowAny()]
        return [IsTaxOfficer()]

    def get(self, request):
        profiles = TaxPayerProfile.objects.all()
        serializer = TaxPayerProfileSerializer(profiles, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = TaxPayerProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class TaxPayerDetailView(APIView):
    permission_classes = [IsOwnerOrOfficer]

    def get_object(self, tin):
        obj = get_object_or_404(TaxPayerProfile, tin=tin)
        # trigger permission check
        self.check_object_permissions(self.request, obj) 
        return obj
    
    def get(self, request, tin):
        profile = self.get_object(tin)
        serializer = TaxPayerProfileSerializer(profile)
        return Response(serializer.data)
    
    def put(self, request,tin):
        profile = self.get_object(tin)
        serializer = TaxPayerProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, tin):
        profile = self.get_object(tin)
        user = profile.user
        # if User is deleted, Profile is deleted
        # if Profile is deleted, User might remain unless explicitely handeled
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Tax Officer Views

class TaxOfficerListCreateView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        profiles = TaxOfficerProfile.objects.all()
        serializer = TaxOfficerProfileSerializer(profiles, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = TaxOfficerProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaxOfficerDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, officer_id):
        obj = get_object_or_404(TaxOfficerProfile, officer_id)
        if not self.request.user.is_superuser:
            if not hasattr(self.request.user, 'taxofficerprofile') or \
               self.request.user.taxofficerprofile.officer_id != officer_id:
                self.permission_denied(self.request)
        return obj
    
    def get(self, request, officer_id):
        profile = self.get_object(officer_id)
        serializer = TaxOfficerProfileSerializer(profile)
        return Response(serializer.data)
    
    def put(self, request, officer_id):
        profile = self.get_object(officer_id)
        serializer = TaxOfficerProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, officer_id):
        profile = self.get_object(officer_id)
        user = profile.user

        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

# Login View
class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer