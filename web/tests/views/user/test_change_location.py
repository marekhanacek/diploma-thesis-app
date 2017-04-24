from django.test import TestCase
from django.urls.base import reverse


class UserChangeLocationTests(TestCase):
    fixtures = ['initial_data.json']

    def test_preferences(self):
        params = {
            'lat': 123,
            'lng': 12,
            'radius': 20,
            'address': 'Praha',
        }
        response = self.client.post(reverse('change_location'), params)
        self.assertEqual(response.status_code, 302)
        input_offer = self.client.session['input_offer']
        self.assertEqual(input_offer['lat'], params['lat'])
        self.assertEqual(input_offer['lng'], params['lng'])
        self.assertEqual(input_offer['radius'], params['radius'])
        self.assertEqual(input_offer['address'], params['address'])
