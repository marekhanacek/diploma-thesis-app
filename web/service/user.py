from django.db.models.query_utils import Q

from web.models import Offer
from web.service.offer import get_offer_visible_feedbacks, is_feedback_visible


def save_user_location_to_session(session, lat, lng, radius, address):
    if 'input_offer' not in session:
        session['input_offer'] = {}
    session['input_offer']['lat'] = float(lat)
    session['input_offer']['lng'] = float(lng)
    session['input_offer']['radius'] = float(radius)
    session['input_offer']['address'] = address
    session.modified = True


def get_number_of_offers(user):
    return user.created_offers.count() + user.responded_offers.count()


def is_verified(user):
    return False if len(get_user_feedbacks(user)) < 2 else get_user_stars(user) > 3


def get_user_feedbacks(user):
    feedbacks = user.feedbacks_responded.all()
    array = []
    for feedback in feedbacks:
        if is_feedback_visible(feedback):
            array.append(feedback)
    return array
    #
    # offers = Offer.objects.filter(
    #     Q(user_created=user) | Q(user_responded=user)
    # )
    # feedbacks = []
    # for offer in offers:
    #     for feedback in get_offer_visible_feedbacks(offer):
    #         if feedback.user_created != user:
    #             feedbacks.append(feedback)
    # return feedbacks


def get_user_stars(user):
    feedbacks = get_user_feedbacks(user)
    stars = 0
    for feedback in feedbacks:
        stars += feedback.stars
    return stars / len(feedbacks) if len(feedbacks) else 0
