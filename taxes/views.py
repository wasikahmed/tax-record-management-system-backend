from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from users.permissions import IsTaxPayer, IsTaxOfficer, IsOwnerOrOfficer
from .models import TaxReturn, Payment
from .serializers import TaxReturnSerializer, PaymentSerializer


# Tax Return Views

class TaxReturnListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # filtering logic
        if hasattr(request.user, 'taxofficerprofile') or request.user.is_superuser:
            # Officer sees all
            returns = TaxReturn.objects.all()
        elif hasattr(request.user, 'taxpayerprofile'):
            # Taxpayer sees own
            returns = TaxReturn.objects.filter(taxpayer=request.user.taxpayerprofile)
        else:
            return Response([], status=200)

        serializer = TaxReturnSerializer(returns, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        # only Taxpayers or Admins can file tax return
        if not (hasattr(request.user, 'taxpayerprofile') or request.user.is_superuser):
            return Response({"detail": "Only taxpayers can file returns."}, status=403)

        # Auto-assign the taxpayer field if not provided
        data = request.data.copy()
        if hasattr(request.user, 'taxpayerprofile'):
            data['taxpayer'] = request.user.taxpayerprofile.tin
        
        serializer = TaxReturnSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class TaxReturnDetailView(APIView):
    permission_classes = [IsOwnerOrOfficer]
    
    def get_object(self, tax_return_id):
        obj = get_object_or_404(TaxReturn, tax_return_id)
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, tax_return_id):
        tax_return = self.get_object(tax_return_id)
        serializer = TaxReturnSerializer(tax_return, data=request.data)
        
    def put(self, request, tax_return_id):
        tax_return = self.get_object(tax_return_id)
        serializer = TaxReturnSerializer(tax_return, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, tax_return_id):
        if not request.user.is_superuser:
            return Response({"detail": "Not allowed."}, status=status.HTTP_403_FORBIDDEN)

        tax_return = self.get_object(tax_return_id)
        tax_return.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

# Payment Views

class PaymentListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if hasattr(request.user, 'taxofficerprofile'):
            payments = Payment.objects.all()
        elif hasattr(request.user, 'taxpayerprofile'):
            # lookup: Payment -> TaxReturn -> Taxpayer
            payments = Payment.objects.filter(tax_return__taxpayer=request.user.taxpayerprofile)
        else:
            payments = []
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        # Check if the user owns the return they are paying for
        return_id = request.data.get('tax_return')
        if not return_id:
             return Response({"detail": "tax_return ID required"}, status=400)
        
        tax_return = get_object_or_404(TaxReturn, pk=return_id)
        
        # Verify ownership
        if hasattr(request.user, 'taxpayerprofile'):
            if tax_return.taxpayer != request.user.taxpayerprofile:
                 return Response({"detail": "You cannot pay for someone else's return."}, status=403)

        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)