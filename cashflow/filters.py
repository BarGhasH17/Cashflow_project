import django_filters
from django import forms
from .models import CashFlowRecord


class CashFlowFilter(django_filters.FilterSet):
    """
    FilterSet for querying CashFlowRecord instances with advanced filtering capabilities.
    Provides range-based date filtering and exact match filters for related models.
    
    Features:
    - Date range filtering with custom widget
    - Consistent styling for all filter controls
    - Exact match filters for status, type, category, and subcategory
    """
    
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
        """
        Initialize the filter with consistent Bootstrap form styling.
        Applies uniform 'form-select' classes to all select inputs.
        """
        super().__init__(*args, **kwargs)
        
        # Apply consistent styling to all select inputs
        for field_name, field in self.filters.items():
            if hasattr(field, 'field') and isinstance(field.field.widget, forms.Select):
                field.field.widget.attrs.update({
                    'class': 'form-select form-select-sm'
                })