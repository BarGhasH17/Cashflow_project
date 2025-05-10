from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from .models import CashFlowRecord, Status, Type, Category, Subcategory
from .filters import CashFlowFilter
from .forms import CashFlowForm
from django.views.decorators.http import require_POST


def record_list(request):
    """
    Display and filter cash flow records.
    Returns a paginated list of records ordered by date (newest first).
    """
    records = CashFlowRecord.objects.all().order_by('-date')
    record_filter = CashFlowFilter(request.GET, queryset=records)
    
    return render(request, 'cashflow/record_list.html', {
        'filter': record_filter,
        'records': record_filter.qs
    })


def add_record(request):
    """
    Handle cash flow record creation.
    On POST: Validates form data and creates new record if valid.
    On GET: Returns empty form for record creation.
    """
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
    """
    API endpoint for adding new statuses via AJAX.
    Expects POST with 'name' parameter.
    Returns JSON with new status data or error message.
    """
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
    """
    API endpoint for adding new types via AJAX.
    Expects POST with 'name' parameter.
    Returns JSON with new type data or error message.
    """
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
    """
    API endpoint for adding new categories via AJAX.
    Expects POST with 'name' parameter.
    Returns JSON with new category data or validation errors.
    """
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        
        if not name:
            return JsonResponse({'error': 'Name is required'}, status=400)
            
        try:
            category = Category.objects.create(name=name)
            return JsonResponse({
                'id': category.id,
                'name': category.name
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)


@csrf_exempt
def quick_add_subcategory(request):
    """
    API endpoint for adding new subcategories via AJAX.
    Expects POST with 'category_id' and 'name' parameters.
    Returns JSON with new subcategory data or validation errors.
    """
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
    """
    API endpoint for fetching categories filtered by type.
    Expects GET parameter 'type_id'.
    Returns JSON list of categories with id and name.
    """
    type_id = request.GET.get('type_id')
    categories = Category.objects.filter(type_id=type_id).values('id', 'name')
    return JsonResponse(list(categories), safe=False)


def get_subcategories(request):
    """
    API endpoint for fetching subcategories filtered by category.
    Expects GET parameter 'category_id'.
    Returns JSON list of subcategories with id and name.
    """
    category_id = request.GET.get('category_id')
    subcategories = Subcategory.objects.filter(category_id=category_id).values('id', 'name')
    return JsonResponse(list(subcategories), safe=False)

@require_POST
def delete_record(request, pk):
    """
    Handle DELETE requests for CashFlowRecord instances.
    
    This view safely deletes a cash flow record after validating:
    - The request method is POST (enforced by decorator)
    - The record exists in the database
    - The operation completes successfully

    Args:
        request: HttpRequest object
        pk: Primary key of the CashFlowRecord to delete

    Returns:
        JsonResponse: 
            - {'status': 'success'} on successful deletion (200)
            - {'status': 'error', 'message': str} on failure (4xx/5xx)

    Raises:
        Http404: If record doesn't exist (converted to JSON response)
        PermissionDenied: If authorization checks fail (not shown here)
    """
    try:
        # Safely retrieve the record from database
        record = CashFlowRecord.objects.get(pk=pk)

        # Perform the deletion
        record.delete()

        # Return success response
        return JsonResponse({'status': 'success', 'message': f'Record {pk} deleted successfully'})
    
    except CashFlowRecord.DoesNotExist:
        # Handle missing record case
        return JsonResponse({'status': 'error', 'message': f'Record {pk} not found in database'}, status=404)
    
    except Exception as e:
        # Catch-all for other exceptions (database errors, etc)
        return JsonResponse({'status': 'error', 'message': f'Server error: {str(e)}'}, status=500)
