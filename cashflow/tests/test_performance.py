from django.test import TestCase
from django.urls import reverse

class PerformanceTests(TestCase):
    def test_record_list_performance(self):
        with self.assertNumQueries(5):  # or your expected number
            self.client.get(reverse('record_list'))