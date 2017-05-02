from django.test import TestCase

from web.service.offer import get_sorted_offers, get_offer_distance_from
from web.service.offer_sorting_strategies import AmountSortingStrategy, DistanceSortingStrategy, \
    StarsSortingStrategy, RatingsSortingStrategy

# TODO
from web.service.user import get_user_stars


class OfferSortingStrategiesTests(TestCase):
    fixtures = ['initial_data.json']

    def get_offers(self, strategy):
        return get_sorted_offers(
            input_offer={
                'lat': 14,
                'lng': 54,
                'radius': 20000,
            },
            sorting_strategy=strategy,
            currency_from=2,
            currency_to=1,
            amount_from=0,
            amount_to=99999999,
            limit=None,
            user=None
        )

    def test_amount_strategy(self):
        offers = self.get_offers(AmountSortingStrategy())
        previous = offers[:1][0]
        for offer in offers:
            self.assertLessEqual(previous.amount * previous.exchange_rate, offer.amount * offer.exchange_rate)
            previous = offer

    def test_distance_strategy(self):
        offers = self.get_offers(DistanceSortingStrategy())
        previous = offers[:1][0]
        for offer in offers:
            self.assertLessEqual(get_offer_distance_from(previous, 14, 54), get_offer_distance_from(offer, 14, 54))
            previous = offer

    def test_stars_strategy(self):
        offers = self.get_offers(StarsSortingStrategy())
        previous = offers[:1][0]
        for offer in offers:
            self.assertGreaterEqual(get_user_stars(previous.user_created), get_user_stars(offer.user_created))
            previous = offer
