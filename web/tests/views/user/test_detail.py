from django.urls.base import reverse

from web.tests import BaseTestCase


class UserDetailTests(BaseTestCase):
    fixtures = ['initial_data.json']

    def test_redirect_to_my_profile(self):
        user = self.get_user_except()
        self.client.force_login(user)
        response = self.client.get(reverse('user_detail', kwargs={'id': user.id}))
        self.assertEqual(response.status_code, 302)

    def test_detail(self):
        user = self.get_user_except()
        response = self.client.get(reverse('user_detail', kwargs={'id': user.id}))
        self.assertEqual(response.status_code, 200)
