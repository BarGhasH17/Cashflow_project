from django.shortcuts import render, redirect
from .models import CashFlowRecord, Status, Type, Category, Subcategory
from .forms import CashFlowForm  # You'll create this next

def record_list(request):
    records = CashFlowRecord.objects.all()
    return render(request, 'cashflow/record_list.html', {'records': records})

def add_record(request):
    if request.method == 'POST':
        form = CashFlowForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('record_list')
    else:
        form = CashFlowForm()
    return render(request, 'cashflow/add_record.html', {'form': form})