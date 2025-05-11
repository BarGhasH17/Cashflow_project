from django.test import TestCase
from django.urls import reverse

class TemplateTests(TestCase):
    def test_base_template_extends(self):
        response = self.client.get(reverse('record_list'))
        self.assertTemplateUsed(response, 'base.html')
        self.assertContains(response, 'Cash Flow Manager')

    def test_add_record_template_fields(self):
      response = self.client.get(reverse('add_record'))
      self.assertContains(response, 'name="date"')
      self.assertContains(response, 'name="amount"')
      self.assertContains(response, 'name="status"')
      self.assertContains(response, 'name="type"')
      self.assertContains(response, 'name="category"')
      self.assertContains(response, 'name="subcategory"')
      self.assertContains(response, 'name="comment"')