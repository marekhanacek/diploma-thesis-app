from web.service.offer import is_feedback_visible


def save_user_location_to_session(session, lat, lng, radius, address):
    if 'input_offer' not in session:
        session['input_offer'] = {}
    session['input_offer']['lat'] = float(lat)
    session['input_offer']['lng'] = float(lng)
    session['input_offer']['radius'] = int(radius)
    session['input_offer']['address'] = address
    session.modified = True


def save_user_currencies_to_session(session, currency_from, currency_to):
    if 'input_offer' not in session:
        session['input_offer'] = {}
    session['input_offer']['currency_from'] = currency_from
    session['input_offer']['currency_to'] = currency_to
    session.modified = True


def get_number_of_offers(user):
    return user.created_offers.count() + user.responded_offers.count()


def is_verified(user):
    return False if len(get_user_feedbacks(user)) < 2 else get_user_stars(user) > 3


def get_user_feedbacks(user, visible_only=True):
    feedbacks = user.feedbacks_responded.all()

    if not visible_only:
        return feedbacks

    array = []
    for feedback in feedbacks:
        if is_feedback_visible(feedback):
            array.append(feedback)
    return array


def get_user_stars(user):
    feedbacks = get_user_feedbacks(user)
    stars = 0
    for feedback in feedbacks:
        stars += feedback.stars
    return stars / len(feedbacks) if len(feedbacks) else 0
