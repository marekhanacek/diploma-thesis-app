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
