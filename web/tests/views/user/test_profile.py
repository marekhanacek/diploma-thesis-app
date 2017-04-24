from django.urls.base import reverse

from web.tests import BaseTestCase


class UserProfileTests(BaseTestCase):
    fixtures = ['initial_data.json']

    def test_logged(self):
        user = self.get_user_except()
        self.client.force_login(user)
        response = self.client.get(reverse('user_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Your actual offers', 1)
        self.assertContains(response, 'Finished offers', 1)
        self.assertContains(response, 'Change preferences')

    def test_not_logged(self):
        response = self.client.get(reverse('user_profile'))
        self.assertEqual(response.status_code, 302)
