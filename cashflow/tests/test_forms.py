from django.test import TestCase
from cashflow.forms import CashFlowForm
from cashflow.models import Category, Status, Subcategory, Type

class FormTests(TestCase):
    def test_valid_form(self):
        status = Status.objects.create(name="Test")
        type = Type.objects.create(name="Test")
        category = Category.objects.create(name="Test")
        subcategory = Subcategory.objects.create(name="Test", category=category)
        
        form_data = {
            'status': status.id,
            'type': type.id,
            'category': category.id,
            'subcategory': subcategory.id,
            'amount': '100.00',
            'date': '2023-01-01'
        }
        form = CashFlowForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)
        
    def test_invalid_amount(self):
        form_data = {'amount': 'not_a_number'}
        form = CashFlowForm(data=form_data)
        self.assertFalse(form.is_valid())