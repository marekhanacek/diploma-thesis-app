from django.urls.base import reverse

from web.tests import BaseTestCase


class OfferNewTests(BaseTestCase):
    fixtures = ['initial_data.json']

    def test_new_offer_not_logged(self):
        response = self.client.get(reverse('offer_new'))
        self.assertEqual(response.status_code, 302)

    def test_new_offer_logged(self):
        user = self.get_user_except()
        self.client.force_login(user)
        response = self.client.get(reverse('offer_new'))
        self.assertEqual(response.status_code, 200)

    def test_new_offer_logged_post(self):
        params = {
            'lat': 14,
            'lng': 54,
            'radius': 20,
            'amount_from': 25,
            'comment': 'dsadsafsa',
            'currency_from': 1,
            'currency_to': 2,
            'address': 'Praha'
        }
        user = self.get_user_except()
        self.client.force_login(user)
        response = self.client.post(reverse('offer_new'), params)
        self.assertEqual(response.status_code, 302)
