from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import CashFlowRecord, Status, Type, Category, Subcategory
from .filters import CashFlowFilter
from .forms import CashFlowForm


def record_list(request):
    """Display filtered list of cash flow records"""
    records = CashFlowRecord.objects.all().order_by('-date')
    record_filter = CashFlowFilter(request.GET, queryset=records)
    
    return render(request, 'cashflow/record_list.html', {
        'filter': record_filter,
        'records': record_filter.qs
    })


def add_record(request):
    """Handle creation of new cash flow records"""
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
        'categories': Category.objects.all(),
        'subcategories': Subcategory.objects.all()
    })  

@csrf_exempt
def quick_add_status(request):
    """AJAX endpoint for adding new statuses"""
    if request.method == 'POST':
        status_name = request.POST.get('name', '').strip()
        if status_name:
            status, created = Status.objects.get_or_create(name=status_name)
            return JsonResponse({
                'id': status.id, 
                'name': status.name
            })
    return JsonResponse({'error': 'Invalid request'}, status=400)


@csrf_exempt
def quick_add_type(request):
    """AJAX endpoint for adding new types"""
    if request.method == 'POST':
        type_name = request.POST.get('name', '').strip()
        if type_name:
            type_obj, created = Type.objects.get_or_create(name=type_name)
            return JsonResponse({
                'id': type_obj.id, 
                'name': type_obj.name
            })
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def quick_add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        
        if not name:
            return JsonResponse({'error': 'Name is required'}, status=400)
            
        try:
            category = Category.objects.create(
                name=name,
            )
            return JsonResponse({
                'id': category.id,
                'name': category.name
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def quick_add_subcategory(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        name = request.POST.get('name', '').strip()
        
        if not category_id:
            return JsonResponse({'error': 'Category ID is required'}, status=400)
        
        if not name:
            return JsonResponse({'error': 'Name is required'}, status=400)
            
        try:
            subcategory = Subcategory.objects.create(
                name=name,
                category_id=category_id
            )
            return JsonResponse({
                'id': subcategory.id,
                'name': subcategory.name
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def get_categories(request):
    """AJAX endpoint for fetching categories by type"""
    type_id = request.GET.get('type_id')
    categories = Category.objects.filter(type_id=type_id).values('id', 'name')
    return JsonResponse(list(categories), safe=False)


def get_subcategories(request):
    """AJAX endpoint for fetching subcategories by category"""
    category_id = request.GET.get('category_id')
    subcategories = Subcategory.objects.filter(category_id=category_id).values('id', 'name')
    return JsonResponse(list(subcategories), safe=False)