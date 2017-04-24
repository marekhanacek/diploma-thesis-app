from django.urls.base import reverse

from web.tests import BaseTestCase


class UserPreferencesTests(BaseTestCase):
    fixtures = ['initial_data.json']

    def test_logged(self):
        user = self.get_user_except()
        self.client.force_login(user)
        response = self.client.get(reverse('change_preferences'))
        self.assertEqual(response.status_code, 200)

    def test_not_logged(self):
        response = self.client.get(reverse('change_preferences'))
        self.assertEqual(response.status_code, 302)
