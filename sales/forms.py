# sales/forms.py

from django import forms
from django.core.exceptions import ValidationError
from decimal import Decimal
from .models import (
    Customer, Sale, SaleItem, Payment,
    SaleReturn, SaleReturnItem, CreditRecord
)
from inventory.models import Product


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            'first_name', 'last_name', 'tin', 'fin', 'email',
            'address', 'phone_number', 'phone_number_2',
            'city', 'state', 'postal_code',
            'customer_type', 'discount_percent', 'credit_limit', 'notes'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'tin': forms.TextInput(attrs={'class': 'form-control'}),
            'fin': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number_2': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'customer_type': forms.Select(attrs={'class': 'form-control'}),
            'discount_percent': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '100'}),
            'credit_limit': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['customer', 'customer_name', 'discount_percent', 'notes']
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-control'}),
            'customer_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Walk-in customer name'}),
            'discount_percent': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '100'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['customer'].queryset = Customer.objects.filter(is_active=True)
        self.fields['customer'].required = False


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount', 'payment_method', 'reference_number', 'notes']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
            'reference_number': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount and amount <= 0:
            raise ValidationError('Amount must be greater than zero.')
        return amount


class SaleReturnForm(forms.ModelForm):
    class Meta:
        model = SaleReturn
        fields = ['reason', 'notes']
        widgets = {
            'reason': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }


class SaleReturnItemForm(forms.ModelForm):
    class Meta:
        model = SaleReturnItem
        fields = ['quantity', 'reason']
        widgets = {
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'reason': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }


class CustomerSearchForm(forms.Form):
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by name, phone, or email...'
        })
    )
    customer_type = forms.ChoiceField(
        choices=[('', 'All Types')] + list(Customer.CUSTOMER_TYPES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class POSCheckoutForm(forms.Form):
    customer = forms.ModelChoiceField(
        queryset=Customer.objects.filter(is_active=True),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'customer-select'})
    )
    customer_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'customer-name',
            'placeholder': 'Enter customer name for walk-in'
        })
    )
    payment_amount = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'id': 'payment-amount',
            'step': '0.01',
            'min': '0'
        })
    )
    payment_method = forms.ChoiceField(
        choices=Payment.PAYMENT_METHODS,
        initial='cash',
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'payment-method'})
    )
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 2, 'class': 'form-control', 'placeholder': 'Additional notes'})
    )

    def clean(self):
        cleaned_data = super().clean()
        customer = cleaned_data.get('customer')
        customer_name = cleaned_data.get('customer_name', '').strip()
        payment_amount = cleaned_data.get('payment_amount') or Decimal('0')

        if not customer and not customer_name:
            raise ValidationError('Please select a customer or enter a walk-in customer name.')

        if payment_amount < 0:
            raise ValidationError('Payment amount cannot be negative.')

        return cleaned_data


class CreditRecordForm(forms.ModelForm):
    class Meta:
        model = CreditRecord
        fields = ['due_date', 'notes']
        widgets = {
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }


class CreditPaymentForm(forms.Form):
    amount = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'min': '0.01'
        })
    )
    payment_method = forms.ChoiceField(
        choices=Payment.PAYMENT_METHODS,
        initial='cash',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    reference_number = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 2, 'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        self.remaining_balance = kwargs.pop('remaining_balance', None)
        super().__init__(*args, **kwargs)

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount and amount <= 0:
            raise ValidationError('Amount must be greater than zero.')
        if self.remaining_balance and amount and amount > self.remaining_balance:
            raise ValidationError(f'Amount cannot exceed remaining balance of {self.remaining_balance}.')
        return amount


class ConvertProformaForm(forms.Form):
    payment_amount = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        required=False,
        initial=0.00,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'})
    )
    payment_method = forms.ChoiceField(
        choices=Payment.PAYMENT_METHODS,
        initial='cash',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )