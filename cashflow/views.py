from django.shortcuts import render, redirect
from .models import CashFlowRecord, Status, Type, Category, Subcategory
from django.http import JsonResponse
from .filters import CashFlowFilter 
from .forms import CashFlowForm  # You'll create this next
from django.views.decorators.csrf import csrf_exempt

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

def record_list(request):
    # Get all records
    records = CashFlowRecord.objects.all().order_by('-date')  # Newest first
    
    # Apply filters
    record_filter = CashFlowFilter(request.GET, queryset=records)
    
    context = {
        'filter': record_filter,  # Pass the filter to template
        'records': record_filter.qs  
    }
    return render(request, 'cashflow/record_list.html', context)

@csrf_exempt
def quick_add_status(request):
    if request.method == 'POST':
        status_name = request.POST.get('name', '').strip()
        if status_name:
            status, created = Status.objects.get_or_create(name=status_name)
            return JsonResponse({'id': status.id, 'name': status.name})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def quick_add_type(request):
    if request.method == 'POST':
        type_name = request.POST.get('name', '').strip()
        if type_name:
            type_obj, created = Type.objects.get_or_create(name=type_name)
            return JsonResponse({'id': type_obj.id, 'name': type_obj.name})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def add_record(request):
    if request.method == 'POST':
        form = CashFlowForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('record_list')
    else:
        form = CashFlowForm()
    
    return render(request, 'cashflow/add_record.html', {
        'form': form,
        'statuses': Status.objects.all(),
        'types': Type.objects.all(),
    })