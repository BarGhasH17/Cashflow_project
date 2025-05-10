from django import forms
from .models import CashFlowRecord


class CashFlowForm(forms.ModelForm):
    """
    Form for creating and editing CashFlowRecord instances.
    Includes additional fields for dynamically adding new statuses and types.
    
    Attributes:
        new_status: Hidden field for adding new status values on-the-fly
        new_type: Hidden field for adding new type values on-the-fly
    """
    new_status = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control-sm d-none',
            'placeholder': 'New status name',
            'id': 'new-status-input'
        })
    )
    
    new_type = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control-sm d-none',
            'placeholder': 'New type',
            'id': 'new-type-input'
        })
    )

    class Meta:
        model = CashFlowRecord
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'id': 'date-select'
            }),
            'amount': forms.NumberInput(attrs={ 
                'class': 'form-control',
                'id': 'amount-select'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'comment-select',
                'rows': '4'
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