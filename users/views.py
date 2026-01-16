from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import TaxPayerProfile, TaxZone, TaxCategory, TaxOfficerProfile
from .serializers import (
    TaxPayerProfileSerializer,
    TaxZoneSerializer,
    TaxCategorySerializer,
    TaxOfficerProfileSerializer
)


class TaxZoneListCreateView(APIView):
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
    def get_object(self, tin):
        return get_object_or_404(TaxPayerProfile, tin=tin)
    
    def get(self, request, tin):
        profile = self.get_object(tin)
        serializer = TaxPayerProfileSerializer(profile)
        return Response(serializer.data)
    
    def put(self, request,tin):
        profile = self.get_object(tin)
        serializer = TaxPayerProfileSerializer(profile, data=request.data)
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
    def get_object(self, officer_id):
        return get_object_or_404(TaxOfficerProfile, officer_id)
    
    def get(self, request, officer_id):
        profile = self.get_object(officer_id)
        serializer = TaxOfficerProfileSerializer(profile)
        return Response(serializer.data)
    
    def put(self, request, officer_id):
        profile = self.get_object(officer_id)
        serializer = TaxOfficerProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def delete(self, request, officer_id):
        profile = self.get_object(officer_id)
        user = profile.user

        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)