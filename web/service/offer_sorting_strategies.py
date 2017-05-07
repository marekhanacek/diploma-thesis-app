from web.service.offer import get_offer_distance_from
from web.service.user import get_user_stars, get_user_feedbacks


class SortingStrategyInterface:
    def sort_offers(self, offers, amount_from, amount_to, lat, lng):
        raise NotImplementedError("Should have implemented this")


class AmountSortingStrategy(SortingStrategyInterface):
    def sort_offers(self, offers, amount_from, amount_to, lat, lng):
        return sorted(offers, key=lambda x: x.amount * x.exchange_rate)


class DistanceSortingStrategy(SortingStrategyInterface):
    def sort_offers(self, offers, amount_from, amount_to, lat, lng):
        return sorted(offers, key=lambda x: get_offer_distance_from(x, lat, lng))


class StarsSortingStrategy(SortingStrategyInterface):
    def sort_offers(self, offers, amount_from, amount_to, lat, lng):
        return sorted(offers, key=lambda x: get_user_stars(x.user_created), reverse=True)


class RatingsSortingStrategy(SortingStrategyInterface):
    def sort_offers(self, offers, amount_from, amount_to, lat, lng):
        return self.sort(self.add_params(offers, amount_from, amount_to, lat, lng))

    def add_params(self, offers, amount_from, amount_to, lat, lng):
        offers = DistanceSortingStrategy().sort_offers(offers, amount_from, amount_to, lat, lng)
        if len(offers):
            max_distance = get_offer_distance_from(offers[-1], lat, lng)
            min_distance = get_offer_distance_from(offers[0], lat, lng)
            new_offers = []
            for offer in offers:
                setattr(offer, 'rating_stars', self.get_stars_rating(offer))
                setattr(offer, 'rating_distance', self.get_distance_rating(offer, min_distance, max_distance, lat, lng))
                new_offers.append(offer)
            return new_offers
        else:
            return []

    @staticmethod
    def get_stars_rating(offer):
        if len(get_user_feedbacks(offer.user_created)) < 2:
            return 0
        else:
            return {
                0: -2,
                1: -1.5,
                2: -1,
                3: 0.6,
                4: 0.8,
                5: 1,
            }.get(get_user_stars(offer.user_created), 0)

    @staticmethod
    def get_distance_rating(offer, min_distance, max_distance, lat, lng):
        distance_from_min = get_offer_distance_from(offer, lat, lng) - min_distance
        min_max_distance = max_distance - min_distance
        percent = min_max_distance / 100
        return 1 - ((distance_from_min / percent) / 100) if percent else 0

    @staticmethod
    def sort(offers):
        return sorted(
            offers,
            key=lambda x: getattr(x, 'rating_distance') + getattr(x, 'rating_stars'),
            reverse=True
        )


def get_sorting_strategy_by_identificator(identificator):
    if identificator == 'amount':
        return AmountSortingStrategy()
    elif identificator == 'stars':
        return StarsSortingStrategy()
    elif identificator == 'distance':
        return DistanceSortingStrategy()
    else:
        return RatingsSortingStrategy()
