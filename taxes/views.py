from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from users.permissions import IsTaxPayer, IsTaxOfficer, IsOwnerOrOfficer
from .models import TaxReturn, Payment
from .serializers import TaxReturnSerializer, PaymentSerializer


# Tax Return Views

class TaxReturnListCreateView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsTaxPayer()]
        return [IsTaxOfficer()]

    def get(self, request):
        returns = TaxReturn.objects.all()
        serializer = TaxReturnSerializer(returns, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = TaxReturnSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class TaxReturnDetailView(APIView):
    def get_object(self, tax_return_id):
        return get_object_or_404(TaxReturn, tax_return_id)

    def get(self, request, tax_return_id):
        tax_return = self.get_object(tax_return_id)
        serializer = TaxReturnSerializer(tax_return, data=request.data)
        
    def put(self, request, tax_return_id):
        tax_return = self.get_object(tax_return_id)
        serializer = TaxReturnSerializer(tax_return, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, tax_return_id):
        tax_return = self.get_object(tax_return_id)
        tax_return.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

# Payment Views

class PaymentListCreateView(APIView):
    def get(self, request):
        payments = Payment.objects.all()
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)