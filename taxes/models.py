from django.db import models
from users.models import TaxPayerProfile, TaxOfficerProfile, TaxCategory


class TaxReturn(models.Model):
    return_id = models.BigAutoField(primary_key=True)

    # relationships
    taxpayer = models.ForeignKey(TaxPayerProfile, on_delete=models.CASCADE, related_name='tax_returns')
    tax_category = models.ForeignKey(TaxCategory, on_delete=models.SET_NULL, null=True, related_name='returns')
    officer = models.ForeignKey(TaxOfficerProfile, on_delete=models.SET_NULL, null=True, related_name='reviewed_returns')

    assessment_year = models.CharField(max_length=9) # example: "2024-2025"
    total_income = models.DecimalField(max_digits=12, decimal_places=2)
    taxable_amount = models.DecimalField(max_digits=12, decimal_places=2)
    filing_date = models.DateField(auto_now_add=True) # automatically set filing date when created

    def __str__(self):
        return f"Return {self.return_id} ({self.assessment_year})"


class Payment(models.Model):
    payment_id = models.BigAutoField(primary_key=True)

    # relationship
    tax_return = models.OneToOneField(TaxReturn, on_delete=models.CASCADE, related_name='payment')

    amount = models.DecimalField(max_digits=12, decimal_places=2)
    method = models.CharField(max_length=20) # example: Bank, Card, Mobile Banking (Bkash, Nagad)
    status = models.CharField(max_length=20, default='Pending') # Paid, Pending, Failed
    transaction_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.payment_id} - {self.status}"
