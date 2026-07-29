from django import forms
from django.core.exceptions import ValidationError
from decimal import Decimal
from .models import Category, Product, InventoryAdjustment


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'parent', 'description', 'icon', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'parent': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'icon': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'fa-box'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ProductForm(forms.ModelForm):
    markup_percentage = forms.DecimalField(
        max_digits=5,
        decimal_places=2,
        required=False,
        initial=30,
        label='Markup Percentage (%)',
        help_text='Auto-calculates selling price',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
    )

    # Add batch number field
    batch_number = forms.CharField(
        max_length=100,
        required=False,
        label='Batch Number',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter batch number'})
    )

    # Add expiry date field
    expiry_date = forms.DateField(
        required=False,
        label='Expiry Date',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )

    pack_size = forms.CharField(
        max_length=100,
        required=False,
        label='Pack Size',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 10 tablets'})
    )

    class Meta:
        model = Product
        fields = [
            'name',           # Brand Name
            'generic_name',   # Generic Name
            'purchase_price', # Buying Price
            'selling_price',  # Retail Price (auto-calculated)
            'wholesale_price',
            'batch_number',
            'expiry_date',
            'pack_size',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter brand name'}),
            'generic_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter generic name'}),
            'purchase_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'placeholder': '0.00'}),
            'selling_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'placeholder': 'Auto-calculated'}),
            'wholesale_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'placeholder': '0.00'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make selling price optional (auto-calculated)
        self.fields['selling_price'].required = False
        self.fields['generic_name'].required = False

        # Set default values for other required fields
        if not self.instance.pk:
            self.instance.unit = 'piece'
            self.instance.reorder_level = 10
            self.instance.current_stock = 0

    def clean_purchase_price(self):
        purchase_price = self.cleaned_data.get('purchase_price')
        if not purchase_price:
            raise ValidationError('Purchase price is required.')
        if purchase_price <= 0:
            raise ValidationError('Purchase price must be greater than zero.')
        return purchase_price

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise ValidationError('Brand name is required.')
        return name

    def clean(self):
        cleaned_data = super().clean()
        purchase_price = cleaned_data.get('purchase_price')
        selling_price = cleaned_data.get('selling_price')
        markup = cleaned_data.get('markup_percentage')

        # Auto-calculate selling price if not provided
        if purchase_price and not selling_price and markup:
            selling_price = purchase_price * (1 + Decimal(str(markup)) / Decimal('100'))
            selling_price = round(selling_price, 2)
            cleaned_data['selling_price'] = selling_price

        return cleaned_data


class StockAdjustmentForm(forms.ModelForm):
    class Meta:
        model = InventoryAdjustment
        fields = ['product', 'reason', 'quantity', 'notes']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control select2'}),
            'reason': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.filter(is_active=True)

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity and quantity <= 0:
            raise ValidationError('Quantity must be greater than zero.')
        return quantity

    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get('product')
        reason = cleaned_data.get('reason')
        quantity = cleaned_data.get('quantity')

        if product and reason in ['damage', 'expiry', 'theft'] and quantity:
            if product.current_stock < quantity:
                self.add_error('quantity', f'Cannot reduce stock by {quantity}. Only {product.current_stock} items in stock.')

        return cleaned_data


class ProductSearchForm(forms.Form):
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by name, generic name...'
        })
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.filter(is_active=True),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    product_type = forms.ChoiceField(
        choices=[('', 'All Types')] + list(Product.PRODUCT_TYPES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    low_stock = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )