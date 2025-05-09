import django_filters
from django import forms
from .models import CashFlowRecord

class CashFlowFilter(django_filters.FilterSet):
    date = django_filters.DateFromToRangeFilter(
        field_name='date',
        label='Date Range',
        widget=django_filters.widgets.RangeWidget(attrs={
            'type': 'date',
            'class': 'form-control form-control-sm'
        })
    )
    
    class Meta:
        model = CashFlowRecord
        fields = {
            'status': ['exact'],
            'type': ['exact'],
            'category': ['exact'],
            'subcategory': ['exact'],
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Apply consistent styling to all select inputs
        for field_name, field in self.filters.items():
            if hasattr(field, 'field') and isinstance(field.field.widget, forms.Select):
                field.field.widget.attrs.update({
                    'class': 'form-select form-select-sm'
                })