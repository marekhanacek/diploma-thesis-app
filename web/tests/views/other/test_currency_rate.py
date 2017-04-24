from django.test import TestCase
from django.urls.base import reverse


class CurrencyRateTests(TestCase):
    fixtures = ['initial_data.json']

    def test_rate(self):
        response = self.client.get(reverse('exchange_rate', args=[1, 2]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(float(response.content), 0.037696)

    def test_rate_not_found(self):
        response = self.client.get(reverse('exchange_rate', args=[0, 1]))
        self.assertEqual(response.status_code, 404)
