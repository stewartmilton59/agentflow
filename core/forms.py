from django import forms
from .models import Company, SystemSetting, Backup

class CompanyForm(forms.ModelForm):
    """Company information form"""
    class Meta:
        model = Company
        fields = [
            'name', 'p_o_box', 'legal_name', 'tax_id', 'registration_no',
            'email', 'phone', 'mobile', 'website',
            'address', 'city', 'state', 'postal_code', 'country',
            'location',
            'logo', 'favicon',
            'primary_color', 'color_changes_remaining',
            'currency', 'currency_symbol',
            'invoice_prefix', 'invoice_footer_text',
            'enable_loyalty', 'enable_prescription', 'enable_email_notifications',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'p_o_box': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. P.O.BOX 1719'}),
            'legal_name': forms.TextInput(attrs={'class': 'form-control'}),
            'tax_id': forms.TextInput(attrs={'class': 'form-control'}),
            'registration_no': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Kariakoo, Dar es salaam, Tanzania'}),
            'logo': forms.FileInput(attrs={'class': 'form-control'}),
            'favicon': forms.FileInput(attrs={'class': 'form-control'}),
            'primary_color': forms.TextInput(attrs={'class': 'form-control', 'type': 'color'}),
            'color_changes_remaining': forms.NumberInput(attrs={'class': 'form-control', 'readonly': True}),
            'currency': forms.TextInput(attrs={'class': 'form-control'}),
            'currency_symbol': forms.TextInput(attrs={'class': 'form-control'}),
            'invoice_prefix': forms.TextInput(attrs={'class': 'form-control'}),
            'invoice_footer_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'enable_loyalty': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'enable_prescription': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'enable_email_notifications': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_primary_color(self):
        color = self.cleaned_data.get('primary_color')
        if self.instance.pk and self.instance.color_changes_remaining <= 0:
            if color != self.instance.primary_color:
                raise forms.ValidationError(
                    'You have used all 5 allowed color changes. Cannot change color anymore.'
                )
        return color

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.instance.pk and self.instance.color_changes_remaining > 0:
            new_color = self.cleaned_data.get('primary_color')
            if new_color and new_color != self.instance.primary_color:
                instance.color_changes_remaining = self.instance.color_changes_remaining - 1
        if commit:
            instance.save()
        return instance

class SystemSettingForm(forms.ModelForm):
    """System setting form"""
    class Meta:
        model = SystemSetting
        fields = ['setting_key', 'setting_value', 'description']
        widgets = {
            'setting_key': forms.TextInput(attrs={'class': 'form-control'}),
            'setting_value': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

class BackupForm(forms.ModelForm):
    """Backup creation form"""
    class Meta:
        model = Backup
        fields = ['name', 'backup_type']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Weekly Backup - Jan 2025'}),
            'backup_type': forms.Select(attrs={'class': 'form-control'}),
        }