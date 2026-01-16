from django.db import models
from users.models import TaxPayerProfile, TaxOfficerProfile

class SupportTicket(models.Model):
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
    ]

    ticket_id = models.BigAutoField(primary_key=True)
    
    # Relationships
    taxpayer = models.ForeignKey(TaxPayerProfile, on_delete=models.CASCADE, related_name='tickets')
    assigned_officer = models.ForeignKey(TaxOfficerProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tickets')

    # Ticket Details
    subject = models.CharField(max_length=100)
    description = models.TextField()
    priority = models.CharField(max_length=20, default='Medium') # Low, Medium, High
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Open')
    
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Ticket {self.ticket_id}: {self.subject}"