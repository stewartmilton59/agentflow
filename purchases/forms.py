from django import forms
from decimal import Decimal
from .models import PurchaseOrder, PurchaseOrderItem
from inventory.models import Product


class PurchaseOrderForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = ['invoice_number', 'supplier_name', 'notes']
        widgets = {
            'invoice_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Invoice / receipt number'}),
            'supplier_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company name'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Optional notes about this purchase'}),
        }


class PurchaseOrderItemForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrderItem
        fields = ['product', 'quantity', 'unit_price', 'markup_percent', 'selling_price', 'batch_number', 'expiry_date']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control product-select', 'style': 'width:100%'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'value': '1'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'markup_percent': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '100'}),
            'selling_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'batch_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Batch number'}),
            'expiry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.filter(is_active=True).order_by('name')
        self.fields['unit_price'].required = False
        self.fields['markup_percent'].required = False
        self.fields['selling_price'].required = False
        self.fields['batch_number'].required = False
        self.fields['expiry_date'].required = False
        self.fields['quantity'].initial = 1

    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get('product')
        quantity = cleaned_data.get('quantity')
        unit_price = cleaned_data.get('unit_price')
        markup_percent = cleaned_data.get('markup_percent') or Decimal('0')
        selling_price = cleaned_data.get('selling_price')

        if product and quantity and quantity <= 0:
            self.add_error('quantity', 'Quantity must be greater than zero')

        if unit_price in (None, Decimal('0'), 0):
            if product and product.purchase_price:
                cleaned_data['unit_price'] = product.purchase_price
            else:
                cleaned_data['unit_price'] = Decimal('0')

        unit_price = cleaned_data.get('unit_price') or Decimal('0')

        if not selling_price and markup_percent:
            cleaned_data['selling_price'] = Decimal(str(unit_price)) * (Decimal('1') + (markup_percent / Decimal('100')))

        if not cleaned_data.get('selling_price'):
            if product and product.selling_price:
                cleaned_data['selling_price'] = product.selling_price
            else:
                cleaned_data['selling_price'] = unit_price

        return cleaned_data