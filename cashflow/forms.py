from django import forms
from .models import CashFlowRecord
from django.utils.translation import gettext_lazy as _


class CashFlowForm(forms.ModelForm):
    """
    Form for creating and editing CashFlowRecord instances.
    Includes additional fields for dynamically adding new statuses and types.
    
    Attributes:
        new_status: Hidden field for adding new status values on-the-fly
        new_type: Hidden field for adding new type values on-the-fly
    """

    class Meta:
        model = CashFlowRecord
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(
                format='%Y-%m-%d', 
                attrs={
                'type': 'date',
                'class': 'form-control',
                'id': 'date-select'
            }),
            'amount': forms.NumberInput(attrs={ 
                'class': 'form-control',
                'id': 'amount-select',
                'placeholder': _('Enter amount...'),

            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'comment-select',
                'rows': '4',
                'placeholder': _('Write something...'),
            }),
        }

    def __init__(self, *args, **kwargs):
        """
        Initialize form with custom widget attributes for select fields.
        """
        super().__init__(*args, **kwargs)
        self.fields['status'].widget.attrs.update({
            'class': 'form-select-sm',
            'id': 'status-select'
        })
        self.fields['type'].widget.attrs.update({
            'class': 'form-select-sm',
            'id': 'type-select'
        })
    def clean_amount(self):
        """Validate that amount is positive"""
        amount = self.cleaned_data.get('amount')
        if amount and amount <= 0:
            raise forms.ValidationError("Amount must be greater than zero")
        return amount

    def clean(self):
        """Ensure all required relationships are set"""
        cleaned_data = super().clean()
        required_fields = ['status', 'type', 'category', 'subcategory']
        for field in required_fields:
            if not cleaned_data.get(field):
                self.add_error(field, "This field is required")
        return cleaned_data