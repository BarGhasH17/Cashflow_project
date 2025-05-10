from django.test import LiveServerTestCase
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from cashflow.models import Category, Subcategory

class JSTests(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser = Chrome()
        
    def test_dynamic_subcategory_load(self):
        # First create test categories
        category = Category.objects.create(name="Test Category")
        Subcategory.objects.create(name="Test Sub", category=category)
        
        self.browser.get(f"{self.live_server_url}/add/")
        category_select = Select(self.browser.find_element(By.ID, 'id_category'))
        category_select.select_by_visible_text("Test Category")
        
    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()