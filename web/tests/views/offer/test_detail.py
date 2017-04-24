from django.urls.base import reverse

from web.tests import BaseTestCase


class OfferDetailTests(BaseTestCase):
    fixtures = ['initial_data.json']

    def test_not_found(self):
        response = self.client.get(reverse('offer_detail', args=[0]))
        self.assertEqual(response.status_code, 404)

    # awaiting acceptace

    def test_awaiting_acceptance_not_logged(self):
        offer = self.get_offer_awaiting_acceptance()
        response = self.client.get(reverse('offer_detail', args=[offer.id]))
        self.assertEqual(response.status_code, 200)

    def test_awaiting_acceptance_logged_created(self):
        offer = self.get_offer_awaiting_acceptance()
        self.client.force_login(offer.user_created)
        response = self.client.get(reverse('offer_detail', args=[offer.id]))
        self.assertEqual(response.status_code, 200)

    def test_awaiting_acceptance_logged_other(self):
        offer = self.get_offer_awaiting_acceptance()
        user = self.get_user_except([offer.user_created])
        self.client.force_login(user)
        response = self.client.get(reverse('offer_detail', args=[offer.id]))
        self.assertEqual(response.status_code, 200)

    # awaiting approval

    def test_awaiting_approval_not_logged(self):
        offer = self.get_offer_awaiting_approval()
        response = self.client.get(reverse('offer_detail', args=[offer.id]))
        self.assertEqual(response.status_code, 302)

    def test_awaiting_approval_logged_created(self):
        offer = self.get_offer_awaiting_approval()
        self.client.force_login(offer.user_created)
        response = self.client.get(reverse('offer_detail', args=[offer.id]))
        self.assertEqual(response.status_code, 200)

    def test_awaiting_approval_logged_responded(self):
        offer = self.get_offer_awaiting_approval()
        self.client.force_login(offer.user_responded)
        response = self.client.get(reverse('offer_detail', args=[offer.id]))
        self.assertEqual(response.status_code, 200)

    def test_awaiting_approval_logged_other(self):
        offer = self.get_offer_awaiting_approval()
        user = self.get_user_except([offer.user_created, offer.user_responded])
        self.client.force_login(user)
        response = self.client.get(reverse('offer_detail', args=[offer.id]))
        self.assertEqual(response.status_code, 302)

    # ready to exchange

    def test_ready_to_exchange_not_logged(self):
        offer = self.get_offer_ready_to_exchange()
        response = self.client.get(reverse('offer_detail', args=[offer.id]))
        self.assertEqual(response.status_code, 302)

    def test_ready_to_exchange_logged_created(self):
        offer = self.get_offer_ready_to_exchange()
        self.client.force_login(offer.user_created)
        response = self.client.get(reverse('offer_detail', args=[offer.id]))
        self.assertEqual(response.status_code, 200)

    def test_ready_to_exchange_logged_responded(self):
        offer = self.get_offer_ready_to_exchange()
        self.client.force_login(offer.user_responded)
        response = self.client.get(reverse('offer_detail', args=[offer.id]))
        self.assertEqual(response.status_code, 200)

    def test_ready_to_exchange_logged_other(self):
        offer = self.get_offer_ready_to_exchange()
        user = self.get_user_except([offer.user_created, offer.user_responded])
        self.client.force_login(user)
        response = self.client.get(reverse('offer_detail', args=[offer.id]))
        self.assertEqual(response.status_code, 302)

    # finished

    def test_complete_not_logged(self):
        offer = self.get_offer_finished()
        response = self.client.get(reverse('offer_detail', args=[offer.id]))
        self.assertEqual(response.status_code, 302)

    def test_complete_logged_created(self):
        offer = self.get_offer_finished()
        self.client.force_login(offer.user_created)
        response = self.client.get(reverse('offer_detail', args=[offer.id]))
        self.assertEqual(response.status_code, 200)

    def test_complete_logged_responded(self):
        offer = self.get_offer_finished()
        self.client.force_login(offer.user_responded)
        response = self.client.get(reverse('offer_detail', args=[offer.id]))
        self.assertEqual(response.status_code, 200)

    def test_complete_logged_other(self):
        offer = self.get_offer_finished()
        user = self.get_user_except([offer.user_created, offer.user_responded])
        self.client.force_login(user)
        response = self.client.get(reverse('offer_detail', args=[offer.id]))
        self.assertEqual(response.status_code, 302)

    # deleted

    def test_deleted_not_logged(self):
        offer = self.get_offer_deleted()
        response = self.client.get(reverse('offer_detail', args=[offer.id]))
        self.assertEqual(response.status_code, 302)

    def test_deleted_logged_created(self):
        offer = self.get_offer_deleted()
        self.client.force_login(offer.user_created)
        response = self.client.get(reverse('offer_detail', args=[offer.id]))
        self.assertEqual(response.status_code, 200)

    def test_deleted_logged_other(self):
        offer = self.get_offer_deleted()
        user = self.get_user_except([offer.user_created])
        self.client.force_login(user)
        response = self.client.get(reverse('offer_detail', args=[offer.id]))
        self.assertEqual(response.status_code, 302)