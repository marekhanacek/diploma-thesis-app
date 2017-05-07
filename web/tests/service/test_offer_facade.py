from django.contrib.auth.models import User

from dip import settings
from web.models import Offer, Feedback, Currency
from web.service.offer import create_offer, get_base_offers, get_offers_waiting_for_user_reaction, \
    get_offers_waiting_for_other_user_reaction, get_exchange_rate, get_finished_offers, get_history_of_users, \
    is_offer_waiting_for_user_reaction, is_offer_waiting_for_other_user_reaction, is_feedback_visible, \
    get_offer_visible_feedbacks
from web.tests import BaseTestCase


class OfferFacadeTests(BaseTestCase):
    fixtures = ['initial_data.json']

    def test_create_offer(self):
        params = {
            'lat': 12.3,
            'lng': 21.0,
            'radius': 22,
            'amount': 22,
            'comment': 'Test comment',
            'currency_from': Currency.objects.get(pk=1),
            'currency_to': Currency.objects.get(pk=2),
            'user_created': User.objects.get(pk=1),
            'address': 'Praha'
        }
        count_before = Offer.objects.count()
        offer = create_offer(
            lat=params['lat'],
            lng=params['lng'],
            radius=params['radius'],
            amount=params['amount'],
            comment=params['comment'],
            currency_from=params['currency_from'],
            currency_to=params['currency_to'],
            user_created=params['user_created'],
            address=params['address']
        )
        self.assertEqual(count_before + 1, Offer.objects.count())
        self.assertEqual(offer.lat, params['lat'])
        self.assertEqual(offer.lng, params['lng'])
        self.assertEqual(offer.radius, params['radius'])
        self.assertEqual(offer.amount, params['amount'])
        self.assertEqual(offer.comment, params['comment'])
        self.assertEqual(offer.currency_from, params['currency_from'])
        self.assertEqual(offer.currency_to, params['currency_to'])
        self.assertEqual(offer.user_created, params['user_created'])
        self.assertIsNone(offer.user_responded)
        self.assertEqual(offer.address, params['address'])
        self.assertEqual(offer.status.id, settings.STATUS_AWAITING_ACCEPTANCE)

    def test_get_base_offers(self):
        offers = get_base_offers(
            currency_from=1,
            currency_to=2,
            minus_amount=0,
            plus_amount=99999999,
            user=None
        )
        self.assertEqual(len(offers), 9)

    def test_get_offers_waiting_for_user_reaction(self):
        user = User.objects.get(pk=1)
        offers = get_offers_waiting_for_user_reaction(user)
        self.assertEqual(len(offers), 1)

    def test_get_offers_waiting_for_other_user_reaction(self):
        user = User.objects.get(pk=1)
        offers = get_offers_waiting_for_other_user_reaction(user)
        self.assertEqual(len(offers), 5)

    def test_get_exchange_rate(self):
        rate = get_exchange_rate(1, 2)
        self.assertEqual(rate, 0.037696)

    def test_get_finished_offers(self):
        user = User.objects.get(pk=1)
        offers = get_finished_offers(user)
        self.assertEqual(len(offers), 2)

    def test_get_history_of_users(self):
        first = User.objects.get(pk=1)
        second = User.objects.get(pk=2)
        offers = get_history_of_users(first, second)
        self.assertEqual(len(offers), 1)

    def test_is_offer_waiting_for_user_reaction(self):
        offer = self.get_offer_awaiting_acceptance()
        self.assertFalse(is_offer_waiting_for_user_reaction(offer, offer.user_created))

        offer = self.get_offer_awaiting_approval()
        self.assertTrue(is_offer_waiting_for_user_reaction(offer, offer.user_created))
        self.assertFalse(is_offer_waiting_for_user_reaction(offer, offer.user_responded))

        offer = self.get_offer_ready_to_exchange()
        self.assertTrue(is_offer_waiting_for_user_reaction(offer, offer.user_created))
        self.assertTrue(is_offer_waiting_for_user_reaction(offer, offer.user_responded))

    def test_is_offer_waiting_for_other_user_reaction(self):
        user = User.objects.get(pk=1)
        offer = Offer.objects.get(pk=1)
        self.assertFalse(is_offer_waiting_for_other_user_reaction(offer, user))

    def test_is_feedback_visible(self):
        feedback = Feedback.objects.get(pk=1)
        self.assertTrue(is_feedback_visible(feedback))

    def test_get_offer_visible_feedbacks(self):
        offer = Offer.objects.get(pk=1)
        feedbacks = get_offer_visible_feedbacks(offer)
        self.assertEqual(len(feedbacks), 1)
