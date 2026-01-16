from django.urls import path
from .views import TaxReturnListCreateView, TaxReturnDetailView, PaymentListCreateView


urlpatterns = [
    path('returns/', TaxReturnListCreateView.as_view(), name='tax-return-list'),
    path('returns/<int:pk>/', TaxReturnDetailView.as_view(), name='tax-return-detail'),
    path('payments/', PaymentListCreateView.as_view(), name='payment-list'),
]