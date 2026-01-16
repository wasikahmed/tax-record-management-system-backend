from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import SupportTicket
from .serializers import SupportTicketSerializer


class SupportTicketListCreateView(APIView):
    def get(self, request):
        tickets = SupportTicket.objects.all()
        serializer = SupportTicketSerializer(tickets, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SupportTicketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class SupportTicketDetailView(APIView):
    def get_object(self, pk):
        return get_object_or_404(SupportTicket, pk=pk)

    def get(self, request, pk):
        ticket = self.get_object(pk)
        serializer = SupportTicketSerializer(ticket)
        return Response(serializer.data)

    def put(self, request, pk):
        ticket = self.get_object(pk)
        serializer = SupportTicketSerializer(ticket, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        ticket = self.get_object(pk)
        ticket.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)