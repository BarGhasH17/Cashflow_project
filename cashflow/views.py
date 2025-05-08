from django.shortcuts import render, redirect
from .models import CashFlowRecord, Status, Type, Category, Subcategory
from django.http import JsonResponse
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

def get_categories(request):
    type_id = request.GET.get('type_id')
    categories = Category.objects.filter(type_id=type_id).values('id', 'name')
    return JsonResponse(list(categories), safe=False)

def get_subcategories(request):
    category_id = request.GET.get('category_id')
    subcategories = Subcategory.objects.filter(category_id=category_id).values('id', 'name')
    return JsonResponse(list(subcategories), safe=False)