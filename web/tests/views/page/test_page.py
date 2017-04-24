from django.test import TestCase
from django.urls.base import reverse


class PageTests(TestCase):
    def test_contact(self):
        response = self.client.get(reverse('page', args=['contact']))
        self.assertEqual(response.status_code, 200)

    def test_terms(self):
        response = self.client.get(reverse('page', args=['terms']))
        self.assertEqual(response.status_code, 200)

    def test_how_it_works(self):
        response = self.client.get(reverse('page', args=['how-it-works']))
        self.assertEqual(response.status_code, 200)

    def test_non_existing(self):
        response = self.client.get(reverse('page', args=['not-existing-page-1234']))
        self.assertEqual(response.status_code, 404)
