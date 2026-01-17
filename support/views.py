from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from users.permissions import IsOwnerOrOfficer
from .models import SupportTicket
from .serializers import SupportTicketSerializer

class SupportTicketListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if hasattr(request.user, 'taxofficerprofile') or request.user.is_superuser:
            tickets = SupportTicket.objects.all()
        elif hasattr(request.user, 'taxpayerprofile'):
            tickets = SupportTicket.objects.filter(taxpayer=request.user.taxpayerprofile)
        else:
            tickets = []
            
        serializer = SupportTicketSerializer(tickets, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data.copy()
        # Auto-assign taxpayer
        if hasattr(request.user, 'taxpayerprofile'):
             data['taxpayer'] = request.user.taxpayerprofile.tin
        
        serializer = SupportTicketSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class SupportTicketDetailView(APIView):
    permission_classes = [IsOwnerOrOfficer]

    def get_object(self, pk):
        obj = get_object_or_404(SupportTicket, pk=pk)
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, pk):
        ticket = self.get_object(pk)
        serializer = SupportTicketSerializer(ticket)
        return Response(serializer.data)

    def put(self, request, pk):
        ticket = self.get_object(pk)
        
        # Permission logic: 
        # Officers can update status/assign.
        # Taxpayers can only update description/subject if status is Open.
        
        serializer = SupportTicketSerializer(ticket, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        ticket = self.get_object(pk)
        ticket.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)