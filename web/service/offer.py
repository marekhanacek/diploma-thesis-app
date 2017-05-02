from django.db.models.aggregates import Min, Max
from django.db.models.expressions import F
from django.db.models.fields import FloatField
from django.db.models.functions.base import Cast
from django.db.models.query_utils import Q
import datetime
from django.utils import timezone

from dip import settings
from web.models import Offer, CurrencyRates, Feedback
from web.service import gps_distance


def create_offer(lat, lng, radius, amount, comment, currency_from, currency_to, user_created,
                 address):
    if currency_from == currency_to:
        raise Exception("Cannon create offer with same currencies")
    if amount < 1:
        raise Exception("Amount must be positive number")

    return Offer.objects.create(
        lat=lat,
        lng=lng,
        radius=radius,
        amount=amount,
        exchange_rate=get_exchange_rate(currency_from, currency_to),
        comment=comment,
        currency_from=currency_from,
        currency_to=currency_to,
        status_id=1,
        user_created=user_created,
        address=address,
    )


def create_feedback(offer, user, comment, stars):
    if not offer.status.is_finished():
        raise Exception('Offer has to be in status FINISHED')
    if user != offer.user_created and user != offer.user_responded:
        raise Exception('User is not attached to this offer')
    if stars < 0 or stars > 5:
        raise Exception('Stars is number between 0 and 5')

    if offer.user_created == user:
        other_user = offer.user_responded
    else:
        other_user = offer.user_created

    return Feedback.objects.create(
        offer=offer,
        user_created=user,
        user_responded=other_user,
        comment=comment,
        stars=stars,
    )


# queries

def get_sorted_offers(input_offer, sorting_strategy, currency_from=None, currency_to=None, amount_from=None,
                      amount_to=None, limit=None, user=None):
    offers = get_base_offers(currency_to, currency_from, amount_from, amount_to, user)
    offers = compute_distance_and_filter(offers, input_offer)
    offers = sorting_strategy.sort_offers(offers, amount_from, amount_to, input_offer['lat'], input_offer['lng'])

    if limit and offers.count > limit:
        offers = offers[0:limit]

    return offers


def get_base_offers(currency_from=None, currency_to=None, minus_amount=None, plus_amount=None, user=None):
    offers = Offer.objects \
        .annotate(total=Cast(F('amount') * F('exchange_rate'), FloatField())) \
        .filter(Q(status=1))

    if currency_from:
        offers = offers.filter(currency_from_id=currency_from)

    if currency_to:
        offers = offers.filter(currency_to_id=currency_to)

    if minus_amount and plus_amount:
        offers = offers.filter(total__range=(minus_amount, plus_amount))

    if user and user.is_authenticated():
        offers = offers.filter(~Q(user_created=user))

    return offers


def get_offers_waiting_for_user_reaction(user):
    offers = Offer.objects.filter(~Q(status=4) & ~Q(status=5)).filter(
        Q(user_created=user) | Q(user_responded=user)
    )
    filtered_offers = []
    for offer in offers:
        if is_offer_waiting_for_user_reaction(offer, user):
            filtered_offers.append(offer)
    return filtered_offers


def get_offers_waiting_for_other_user_reaction(user):
    offers = Offer.objects.filter(~Q(status=settings.STATUS_FINISHED) & ~Q(status=settings.STATUS_DELETED)).filter(
        Q(user_created=user) | Q(user_responded=user)
    )
    filtered_offers = []
    for offer in offers:
        if is_offer_waiting_for_other_user_reaction(offer, user):
            filtered_offers.append(offer)
    return filtered_offers


def get_exchange_rate(currency_from, currency_to):
    rate = CurrencyRates.objects.get(currency_from=currency_from, currency_to=currency_to)
    return rate.rate


def get_finished_offers(user):
    return Offer.objects.filter(status=settings.STATUS_FINISHED).filter(
        Q(user_created=user) | Q(user_responded=user)
    )


def get_history_of_users(first, second):
    return Offer.objects.filter(
        (Q(user_created=first) & Q(user_responded=second)) |
        (Q(user_created=second) & Q(user_responded=first))
    )


# other helping methods

def compute_distance_and_filter(offers, input_offer):
    filtered_offers = []
    for offer in offers:
        distance = gps_distance(float(offer.lat), float(offer.lng), float(input_offer['lat']),
                                float(input_offer['lng']))
        if distance < float(offer.radius) + float(input_offer['radius']):
            filtered_offers.append(offer)
    return filtered_offers


def is_offer_waiting_for_user_reaction(offer, user):
    if offer.status.is_awaiting_approval() and offer.user_created == user:
        return True
    if offer.status.is_ready_to_exchange():
        return True
    return False


def is_offer_waiting_for_other_user_reaction(offer, user):
    if offer.status.is_awaiting_approval() and offer.user_responded == user:
        return True
    if offer.status.is_awaiting_acceptance():
        return True
    return False


def get_minimum_amount_for_currencies(currency_from, currency_to):
    amount = get_base_offers(
        currency_from,
        currency_to
    ).aggregate(Min('total'))['total__min']
    return int(amount) if amount else 0


def get_maximum_amount_for_currencies(currency_from, currency_to):
    amount = get_base_offers(
        currency_from,
        currency_to
    ).aggregate(Max('total'))['total__max']
    return int(amount) if amount else 0


def is_feedback_visible(feedback):
    if Feedback.objects.filter(offer=feedback.offer).count() == 2:
        return True
    else:
        return feedback.created_at < (timezone.now() - datetime.timedelta(days=7))


def get_offer_visible_feedbacks(offer):
    filtered_feedbacks = []
    for feedback in offer.feedbacks.all():
        if is_feedback_visible(feedback):
            filtered_feedbacks.append(feedback)
    return filtered_feedbacks


def get_offer_distance_from(offer, lat, lng):
    return gps_distance(lat, lng, offer.lat, offer.lng)
