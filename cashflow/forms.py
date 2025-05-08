from django import forms
from .models import CashFlowRecord
from django.utils import timezone

class CashFlowForm(forms.ModelForm):
    new_status = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control-sm d-none',
            'placeholder': 'New status name',
            'id': 'new-status-input'
        })
    )
    
    new_type = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control-sm d-none', 
        'placeholder': 'New type',
        'id': 'new-type-input'
    }))

    class Meta:
        model = CashFlowRecord
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].widget.attrs.update({
            'class': 'form-select-sm',
            'id': 'status-select'
        })
        self.fields['type'].widget.attrs.update({
            'class': 'form-select-sm', 
            'id': 'type-select'
        })

    