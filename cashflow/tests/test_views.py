from django.test import TestCase, Client
from django.urls import reverse
from cashflow.models import (Status, Type, 
                           Category, Subcategory,
                           CashFlowRecord)

class ViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Create test data once for all tests"""
        cls.client = Client()
        cls.status = Status.objects.create(name="TestStatus")
        cls.type = Type.objects.create(name="TestType")
        cls.category = Category.objects.create(name="TestCategory")
        cls.subcategory = Subcategory.objects.create(
            name="TestSubcategory",
            category=cls.category
        )
        
    def setUp(self):
        """Run before each test"""
        self.record = CashFlowRecord.objects.create(
            status=self.status,
            type=self.type,
            category=self.category,
            subcategory=self.subcategory,
            amount=100.00,
            date="2023-01-01"
        )

    def test_record_list_view(self):
        """Test record listing page"""
        response = self.client.get(reverse('record_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Cash Flow Records")
        self.assertContains(response, "100.00")

    def test_add_record_view(self):
        """Test record creation page"""
        response = self.client.get(reverse('add_record'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Add Cash Flow Record")

    def test_record_deletion(self):
        """Test record deletion"""
        delete_url = reverse('delete_record', args=[self.record.id])
        
        # First request to get CSRF token
        self.client.get(reverse('record_list'))
        
        response = self.client.post(
            delete_url,
            HTTP_X_CSRFTOKEN=self.client.cookies['csrftoken'].value
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertFalse(CashFlowRecord.objects.filter(id=self.record.id).exists())