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

    def test_add_record_view_get(self):
        response = self.client.get(reverse('add_record'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cashflow/add_record.html')

    def test_edit_record_view_post(self):
        record = CashFlowRecord.objects.create(
            date='2025-05-10',
            amount=100.00,
            status=self.status,
            type=self.type,
            category=self.category,
            subcategory=self.subcategory,
            comment='Initial comment',
        )
        updated_data = {
            'date': '2025-05-11',
            'amount': 150.00,
            'status': self.status.id,
            'type': self.type.id,
            'category': self.category.id,
            'subcategory': self.subcategory.id,
            'comment': 'Updated comment',
        }
        response = self.client.post(reverse('edit_record', args=[record.id]), data=updated_data, follow=True)
        self.assertEqual(response.status_code, 200)
        record.refresh_from_db()
        self.assertEqual(record.amount, 150.00)
        self.assertEqual(record.comment, 'Updated comment')
        # self.assertRedirects(response, 'record_list')

    def test_delete_record_view(self):
        record = CashFlowRecord.objects.create(
            date='2025-05-10',
            amount=100.00,
            status=self.status,
            type=self.type,
            category=self.category,
            subcategory=self.subcategory,
            comment='To be deleted',
        )
        response = self.client.post(reverse('delete_record', args=[record.id]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(CashFlowRecord.objects.filter(id=record.id).exists())