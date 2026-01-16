# from rest_framework import generics, permissions

# from .models import TaxPayerProfile, TaxOfficerProfile
# from .serializers import TaxPayerProfileSerializer, TaxOfficerProfileSerializer

# class TaxPayerListCreateView(generics.ListCreateAPIView):
#     queryset = TaxPayerProfile.objects.all()
#     serializer_class = TaxPayerProfileSerializer

#     def get_permissions(self):
#         if self.request.method == 'POST':
#             return [permissions.AllowAny()]
#         return [permissions.IsAuthenticated()]
    
# class TaxPayerDetailsView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = TaxPayerProfile.objects.all()
#     serializer_class = TaxOfficerProfileSerializer
#     permission_classes = [permissions.AllowAny]
#     lookup_field = 'pk'




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import TaxPayerProfile, TaxZone, TaxCategory
from .serializers import (
    TaxPayerProfileSerializer,
    TaxZoneSerializer,
    TaxCategorySerializer
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
