from django.urls import path
from .views import SupportTicketListCreateView, SupportTicketDetailView

urlpatterns = [
    path('tickets/', SupportTicketListCreateView.as_view(), name='ticket-list'),
    path('tickets/<int:pk>/', SupportTicketDetailView.as_view(), name='ticket-detail'),
]