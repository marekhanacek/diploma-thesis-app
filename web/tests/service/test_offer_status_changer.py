from django.core.exceptions import PermissionDenied

from dip import settings
from web.tests import BaseTestCase
from web.service import offer_status


class OfferStatusChangerTests(BaseTestCase):
    fixtures = ['initial_data.json']

    # delete

    def test_delete_user_created(self):
        offer = self.get_offer_awaiting_acceptance()
        offer_status.delete(offer=offer, user=offer.user_created)
        self.assertEqual(settings.STATUS_DELETED, offer.status_id)

    def test_delete_user_that_not_attached(self):
        offer = self.get_offer_awaiting_acceptance()
        user = self.get_user_except([offer.user_created])

        with self.assertRaises(PermissionDenied):
            offer_status.delete(offer=offer, user=user)

        self.assertEqual(settings.STATUS_AWAITING_ACCEPTANCE, offer.status_id)

    # accept

    def test_accept_user_created(self):
        offer = self.get_offer_awaiting_acceptance()

        with self.assertRaises(PermissionDenied):
            offer_status.accept(offer=offer, user=offer.user_created)

        self.assertEqual(settings.STATUS_AWAITING_ACCEPTANCE, offer.status_id)

    def test_accept_user_that_not_attached(self):
        offer = self.get_offer_awaiting_acceptance()
        user = self.get_user_except([offer.user_created])
        offer_status.accept(offer=offer, user=user)
        self.assertEqual(settings.STATUS_AWAITING_APPROVAL, offer.status_id)
        self.assertEqual(user.id, offer.user_responded.id)

    # approve

    def test_approve_user_created(self):
        offer = self.get_offer_awaiting_approval()
        offer_status.approve(offer=offer, user=offer.user_created)
        self.assertEqual(settings.STATUS_READY_TO_EXCHANGE, offer.status_id)

    def test_approve_user_responded(self):
        offer = self.get_offer_awaiting_approval()

        with self.assertRaises(PermissionDenied):
            offer_status.approve(offer=offer, user=offer.user_responded)

        self.assertEqual(settings.STATUS_AWAITING_APPROVAL, offer.status_id)

    def test_approve_user_that_not_attached(self):
        offer = self.get_offer_awaiting_approval()
        user = self.get_user_except([offer.user_created, offer.user_responded])

        with self.assertRaises(PermissionDenied):
            offer_status.approve(offer=offer, user=user)

        self.assertEqual(settings.STATUS_AWAITING_APPROVAL, offer.status_id)

    # refuse

    def test_refuse_user_created(self):
        offer = self.get_offer_awaiting_approval()
        offer_status.refuse(offer=offer, user=offer.user_created)
        self.assertEqual(settings.STATUS_AWAITING_ACCEPTANCE, offer.status_id)
        self.assertIsNone(offer.user_responded)

    def test_refuse_user_responded(self):
        offer = self.get_offer_awaiting_approval()

        with self.assertRaises(PermissionDenied):
            offer_status.refuse(offer=offer, user=offer.user_responded)

        self.assertEqual(settings.STATUS_AWAITING_APPROVAL, offer.status_id)

    def test_refuse_user_that_not_attached(self):
        offer = self.get_offer_awaiting_approval()
        user = self.get_user_except([offer.user_created, offer.user_responded])

        with self.assertRaises(PermissionDenied):
            offer_status.refuse(offer=offer, user=user)
        self.assertEqual(settings.STATUS_AWAITING_APPROVAL, offer.status_id)

    # already_not_interested

    def test_already_not_interested_user_created(self):
        offer = self.get_offer_awaiting_approval()

        with self.assertRaises(PermissionDenied):
            offer_status.already_not_interested(offer=offer, user=offer.user_created)

        self.assertEqual(settings.STATUS_AWAITING_APPROVAL, offer.status_id)

    def test_already_not_interested_user_responded(self):
        offer = self.get_offer_awaiting_approval()
        offer_status.already_not_interested(offer=offer, user=offer.user_responded)
        self.assertEqual(settings.STATUS_AWAITING_ACCEPTANCE, offer.status_id)
        self.assertIsNone(offer.user_responded)

    def test_already_not_interested_user_that_not_attached(self):
        offer = self.get_offer_awaiting_approval()
        user = self.get_user_except([offer.user_created, offer.user_responded])

        with self.assertRaises(PermissionDenied):
            offer_status.already_not_interested(offer=offer, user=user)

        self.assertEqual(settings.STATUS_AWAITING_APPROVAL, offer.status_id)

    # offer_again

    def test_offer_again_user_created(self):
        offer = self.get_offer_ready_to_exchange()
        offer_status.offer_again(offer=offer, user=offer.user_created)
        self.assertEqual(settings.STATUS_AWAITING_ACCEPTANCE, offer.status_id)
        self.assertIsNone(offer.user_responded)

    def test_offer_again_user_responded(self):
        offer = self.get_offer_ready_to_exchange()
        offer_status.offer_again(offer=offer, user=offer.user_responded)
        self.assertEqual(settings.STATUS_AWAITING_ACCEPTANCE, offer.status_id)
        self.assertIsNone(offer.user_responded)

    def test_offer_again_user_that_not_attached(self):
        offer = self.get_offer_ready_to_exchange()
        user = self.get_user_except([offer.user_created, offer.user_responded])

        with self.assertRaises(PermissionDenied):
            offer_status.offer_again(offer=offer, user=user)
        self.assertEqual(settings.STATUS_READY_TO_EXCHANGE, offer.status_id)

    # complete

    def test_complete_user_created(self):
        offer = self.get_offer_ready_to_exchange()
        offer_status.complete(offer=offer, user=offer.user_created)
        self.assertEqual(settings.STATUS_FINISHED, offer.status_id)

    def test_complete_user_responded(self):
        offer = self.get_offer_ready_to_exchange()
        offer_status.complete(offer=offer, user=offer.user_responded)
        self.assertEqual(settings.STATUS_FINISHED, offer.status_id)

    def test_complete_user_that_not_attached(self):
        offer = self.get_offer_ready_to_exchange()
        user = self.get_user_except([offer.user_created, offer.user_responded])

        with self.assertRaises(PermissionDenied):
            offer_status.complete(offer=offer, user=user)

        self.assertEqual(settings.STATUS_READY_TO_EXCHANGE, offer.status_id)
