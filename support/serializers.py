from rest_framework import serializers
from django.utils import timezone
from .models import SupportTicket

class SupportTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportTicket
        fields = [
            'ticket_id', 'taxpayer', 'assigned_officer', 
            'subject', 'description', 'priority', 
            'status', 'created_at', 'resolved_at'
        ]
        read_only_fields = ['ticket_id', 'created_at', 'resolved_at']

    def update(self, instance, validated_data):
        # Auto-set resolved_at timestamp if status changes to Resolved
        new_status = validated_data.get('status')
        if new_status == 'Resolved' and instance.status != 'Resolved':
            instance.resolved_at = timezone.now()
        
        return super().update(instance, validated_data)