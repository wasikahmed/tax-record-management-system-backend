from rest_framework import generics, permissions

from .models import TaxPayerProfile, TaxOfficerProfile
from .serializers import TaxPayerProfileSerializer, TaxOfficerProfileSerializer

class TaxPayerListCreateView(generics.ListCreateAPIView):
    queryset = TaxPayerProfile.objects.all()
    serializer_class = TaxPayerProfileSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
    
class TaxPayerDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TaxPayerProfile.objects.all()
    serializer_class = TaxOfficerProfileSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'pk'