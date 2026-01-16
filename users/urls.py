from django.urls import path
from .views import (
    TaxPayerListCreateView,
    TaxPayerDetailView,
    TaxZoneListCreateView,
    TaxCategoryListCreateView
)


urlpatterns = [
    path('zones/', TaxZoneListCreateView.as_view(), name='tax-zone-list-create'),
    path('categories/', TaxCategoryListCreateView.as_view(), name='tax-category-list-create'),

    # TaxPayer urls
    path('taxpayers/', TaxPayerListCreateView.as_view(), name='taxpayer-list-create'),
    path('taxpayers/<int:tin>/', TaxPayerDetailView.as_view(), name='taxpayer-detail')
]
