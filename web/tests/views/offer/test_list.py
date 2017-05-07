from django.test import TestCase
from django.urls.base import reverse


class OfferListTests(TestCase):
    fixtures = ['initial_data.json']

    def test_page(self):
        response = self.client.get(reverse('offer_list'))
        self.assertEqual(response.status_code, 200)

    def test_sorting(self):
        response = self.client.get(reverse('offer_sort', args=['amount']))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.session['input_offer']['sort'], 'amount')
        response = self.client.get(reverse('offer_list'))
        self.assertEqual(response.status_code, 200)

    def test_exchange_currencies(self):
        params = {
            'amount_from': 1000,
            'amount_to': 2000,
            'currency_from': 2,
            'currency_to': 3,
        }
        min_amount = None
        max_amount = None

        # pri zmene currency_from nebo currency_to se meze nastavuji na min a max
        response = self.client.post(reverse('offer_list'), params)
        self.assertEqual(response.status_code, 302)
        input_offer = self.client.session['input_offer']
        self.assertEqual(input_offer['amount_from'], min_amount)
        self.assertEqual(input_offer['amount_to'], max_amount)
        self.assertEqual(input_offer['currency_from'], params['currency_from'])
        self.assertEqual(input_offer['currency_to'], params['currency_to'])

        # pri druhem pozadavku se nastavuje pozadovana hodnota
        response = self.client.post(reverse('offer_list'), params)
        self.assertEqual(response.status_code, 302)
        input_offer = self.client.session['input_offer']
        self.assertEqual(input_offer['amount_from'], params['amount_from'])
        self.assertEqual(input_offer['amount_to'], params['amount_to'])
        self.assertEqual(input_offer['currency_from'], params['currency_from'])
        self.assertEqual(input_offer['currency_to'], params['currency_to'])
