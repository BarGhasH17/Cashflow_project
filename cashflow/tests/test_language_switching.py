from django.test import TestCase
from django.urls import reverse
from django.utils.translation import activate
from django.conf import settings

class LanguageSwitchTests(TestCase):
    def test_language_switch_to_russian(self):
        response = self.client.post(reverse('set_language'), data={'language': 'ru', 'next': '/'})
        self.assertEqual(response.status_code, 302)  # Redirect after language change
        # Follow the redirect
        response = self.client.get('/', follow=True)
        self.assertContains(response, 'Денежный поток')  # 'Cash Flow' in Russian

    def test_language_switch_to_english(self):
        response = self.client.post(reverse('set_language'), data={'language': 'en', 'next': '/'})
        self.assertEqual(response.status_code, 302)
        response = self.client.get('/', follow=True)
        self.assertContains(response, 'Cash Flow')


class ViewLanguageTests(TestCase):
    def test_view_in_russian(self):
        response = self.client.post('/i18n/setlang/', {'language': 'ru', 'next': '/'}, follow=True)
        response = self.client.get('/')
        self.assertContains(response, 'Статус')
        response = self.client.post('/i18n/setlang/', {'language': 'en', 'next': '/'}, follow=True)

    def test_view_in_english(self):
        activate('en')
        response = self.client.get('/')
        self.assertContains(response, 'Cash Flow')


class AcceptLanguageHeaderTests(TestCase):
    def test_accept_language_russian(self):
        response = self.client.get('/', HTTP_ACCEPT_LANGUAGE='ru')
        self.assertContains(response, 'Денежный поток')

    def test_accept_language_english(self):
        response = self.client.get('/', HTTP_ACCEPT_LANGUAGE='en')
        self.assertContains(response, 'Cash Flow')


class DefaultLanguageTests(TestCase):
    def test_default_language(self):
        response = self.client.get('/')
        default_language = settings.LANGUAGE_CODE
        if default_language.startswith('ru'):
            self.assertContains(response, 'Денежный поток')
        else:
            self.assertContains(response, 'Cash Flow')


class LanguagePersistenceTests(TestCase):
    def test_language_persistence(self):
        # Set language to Russian
        self.client.post(reverse('set_language'), data={'language': 'ru', 'next': '/'})
        # Subsequent request should be in Russian
        response = self.client.get('/')
        self.assertContains(response, 'Денежный поток')