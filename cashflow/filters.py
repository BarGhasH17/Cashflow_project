import django_filters
from .models import CashFlowRecord
from django import forms

class CashFlowFilter(django_filters.FilterSet):
    date = django_filters.DateFromToRangeFilter(
        field_name='date',
        label='Date Range',
        widget=django_filters.widgets.RangeWidget(attrs={'type': 'date'}))
    
    class Meta:
        model = CashFlowRecord
        fields = {
            'status': ['exact'],
            'type': ['exact'],
            'category': ['exact'],
            'subcategory': ['exact'],
            # Date is already declared above with custom widget
        }