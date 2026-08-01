from django import forms

from .models import Expense, ExpenseCategory


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['category', 'description', 'amount', 'expense_date', 'payment_method', 'paid_to', 'reference_number', 'notes']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Monthly electricity bill'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'expense_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'payment_method': forms.Select(attrs={'class': 'form-select'}),
            'paid_to': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. TANESCO'}),
            'reference_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Receipt / invoice no.'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].required = False
        self.fields['category'].empty_label = 'No category (one-off expense)'
        frequent = ExpenseCategory.objects.filter(is_frequent=True, is_active=True)
        self.fields['category'].help_text = (
            'Select a category for frequent/recurring expenses (e.g. electricity bills). '
            'Leave empty for one-off expenses.'
        )


class ExpenseCategoryForm(forms.ModelForm):
    class Meta:
        model = ExpenseCategory
        fields = ['name', 'description', 'icon', 'color', 'is_frequent', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Electricity Bills'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'icon': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. fas fa-bolt'}),
            'color': forms.TextInput(attrs={'class': 'form-control form-control-color', 'type': 'color'}),
        }
