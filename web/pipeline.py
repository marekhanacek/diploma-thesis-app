from requests import request, HTTPError
from django.core.files.base import ContentFile

from web.models import UserProfile
from web.service.user import save_user_location_to_session, save_user_currencies_to_session


def save_profile_picture(backend, user, response, is_new=False, *args, **kwargs):
    if backend.name == 'facebook':
        if is_new:
            UserProfile.objects.create(user=user)

        url = 'http://graph.facebook.com/{0}/picture'.format(response['id'])

        try:
            response = request('GET', url, params={'type': 'large'})
            response.raise_for_status()
        except HTTPError:
            pass
        else:
            profile = user.userprofile
            profile.profile_photo.save('{0}.jpg'.format(user.id), ContentFile(response.content))
            profile.save()


def save_preferences_to_session(strategy, user, *args, **kwargs):
    save_user_location_to_session(
        session=strategy.session,
        lat=user.userprofile.lat,
        lng=user.userprofile.lng,
        radius=user.userprofile.radius,
        address=user.userprofile.address
    )
    save_user_currencies_to_session(
        session=strategy.session,
        currency_from=user.userprofile.home_currency.id,
        currency_to=user.userprofile.exchange_currency.id
    )
