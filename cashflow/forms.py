from django import forms
from .models import CashFlowRecord

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
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'id': 'date-select'
            }),
            'amount': forms.TextInput(attrs={
                'type': 'number',
                'class': 'form-control',
                'id': 'amount-select'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'comment-select',
                "rows": "4"
            }),
        }
        

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

    