from django.db.utils import IntegrityError
from django.test import TestCase
from cashflow.forms import CashFlowForm
from cashflow.models import Status, Type, Category, Subcategory, CashFlowRecord
from django.core.exceptions import ValidationError
from django.utils import timezone

class ModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Create test data once for all tests"""
        cls.status = Status.objects.create(name="Business")
        cls.type = Type.objects.create(name="Income")
        cls.category = Category.objects.create(name="Sales")
        cls.subcategory = Subcategory.objects.create(
            name="Online",
            category=cls.category
        )
        cls.record = CashFlowRecord.objects.create(
            date=timezone.now().date(),
            status=cls.status,
            type=cls.type,
            category=cls.category,
            subcategory=cls.subcategory,
            amount=1000.00
        )

    def test_status_model(self):
        """Test Status model constraints"""
        self.assertEqual(str(self.status), "Business")
        # Test unique constraint using validate_unique()
        duplicate_status = Status(name="Business")
        with self.assertRaises(ValidationError):
            duplicate_status.validate_unique()

    def test_category_model(self):
        """Test Category model functionality"""
        self.assertEqual(str(self.category), "Sales")
        # Test relationship with subcategories
        self.assertEqual(self.category.subcategory_set.count(), 1)
        self.assertEqual(self.category.subcategory_set.first().name, "Online")

    def test_cashflow_record_validation(self):
        """Test model validation rules through the form"""
        form_data = {
            'status': self.status.id,
            'type': self.type.id,
            'category': self.category.id,
            'subcategory': self.subcategory.id,
            'date': timezone.now().date(),
            'amount': -100.00 
        }
        form = CashFlowForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('amount', form.errors)  

    def test_status_str(self):
      status = Status.objects.create(name='Pending')
      self.assertEqual(str(status), 'Pending')

    def test_type_str(self):
      type = Type.objects.create(name='Pending')
      self.assertEqual(str(type), 'Pending')

    def test_category_str(self):
      category = Category.objects.create(name='Pending')
      self.assertEqual(str(category), 'Pending')

    def test_subcategory_str(self):
      subcategory = Subcategory.objects.create(name='Pending', category=Category.objects.create(name='Pending'))
      self.assertEqual(str(subcategory), 'Pending')

    def test_unique_status_name(self):
      Status.objects.create(name='Approved')
      with self.assertRaises(IntegrityError):
          Status.objects.create(name='Approved')

    def test_unique_type_name(self):
      Type.objects.create(name='Approved')
      with self.assertRaises(IntegrityError):
          Type.objects.create(name='Approved')

    def test_unique_category_name(self):
      Category.objects.create(name='Approved')
      with self.assertRaises(IntegrityError):
          Category.objects.create(name='Approved')

    def test_unique_subcategory_name(self):
      Subcategory.objects.create(name='Approved', category=Category.objects.create(name='Approved'))
      with self.assertRaises(IntegrityError):
          Subcategory.objects.create(name='Approved', category=Category.objects.create(name='Approved'))