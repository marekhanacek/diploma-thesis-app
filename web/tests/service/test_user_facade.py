from web.service.user import save_user_location_to_session, get_number_of_offers, get_user_feedbacks, is_verified
from web.tests import BaseTestCase


class UserFacadeTests(BaseTestCase):
    fixtures = ['initial_data.json']

    def test_save_user_location_to_session(self):
        params = {
            'lat': 123,
            'lng': 156,
            'radius': 80,
            'address': 'Praha'
        }
        session = self.client.session
        save_user_location_to_session(
            session=session,
            lat=params['lat'],
            lng=params['lng'],
            radius=params['radius'],
            address=params['address']
        )
        self.assertEqual(session['input_offer']['lat'], params['lat'])
        self.assertEqual(session['input_offer']['lng'], params['lng'])
        self.assertEqual(session['input_offer']['radius'], params['radius'])
        self.assertEqual(session['input_offer']['address'], params['address'])

    def test_get_number_of_offers(self):
        self.assertEqual(get_number_of_offers(user=self.get_verified_user()), 5)

    def test_get_user_feedbacks(self):
        self.assertEqual(len(get_user_feedbacks(user=self.get_verified_user())), 2)
        self.assertEqual(len(get_user_feedbacks(user=self.get_unverified_user())), 0)

    def test_is_verified(self):
        self.assertTrue(is_verified(user=self.get_verified_user()))
        self.assertFalse(is_verified(user=self.get_unverified_user()))
