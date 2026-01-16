from rest_framework import serializers
from .models import TaxReturn, Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['payment_id', 'tax_return', 'amount', 'method', 'status', 'transaction_time']
        read_only_fields = ['payment_id', 'transaction_time']

class TaxReturnSerializer(serializers.ModelSerializer):
    # We can nest the payment info if it exists
    payment = PaymentSerializer(read_only=True)

    class Meta:
        model = TaxReturn
        fields = [
            'return_id', 'taxpayer', 'tax_category', 'officer',
            'assessment_year', 'total_income', 'taxable_amount', 
            'filing_date', 'payment'
        ]
        read_only_fields = ['return_id', 'filing_date']