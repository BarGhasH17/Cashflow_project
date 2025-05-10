from django.test import TestCase
from django.urls import reverse

class TemplateTests(TestCase):
    def test_base_template_extends(self):
        response = self.client.get(reverse('record_list'))
        self.assertTemplateUsed(response, 'base.html')
        self.assertContains(response, 'Cash Flow Manager')