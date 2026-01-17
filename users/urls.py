from django.urls import path
from .views import (
    TaxPayerListCreateView,
    TaxPayerDetailView,
    TaxZoneListCreateView,
    TaxCategoryListCreateView,
    TaxOfficerListCreateView,
    TaxOfficerDetailView,
    CustomLoginView,
)


urlpatterns = [
    # Auth
    path('auth/login/', CustomLoginView.as_view(), name='auth-login'),

    path('zones/', TaxZoneListCreateView.as_view(), name='zones'),
    path('categories/', TaxCategoryListCreateView.as_view(), name='categories'),

    # TaxPayer urls
    path('taxpayers/', TaxPayerListCreateView.as_view(), name='taxpayers'),
    path('taxpayers/<int:tin>/', TaxPayerDetailView.as_view(), name='taxpayer-detail'),
    path('officers/', TaxOfficerListCreateView.as_view(), name='officers'),
    path('officers/<int:officer_id>/', TaxOfficerDetailView.as_view(), name='officer-detail'),
    ]
