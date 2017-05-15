from django.contrib.auth.models import User

from dip import settings
from web.service.offer import get_offers_waiting_for_user_reaction


def template_variables(request):
    marek = User.objects.get(pk=100)
    return {
        'STATUS_AWAITING_ACCEPTANCE': settings.STATUS_AWAITING_ACCEPTANCE,
        'STATUS_AWAITING_APPROVAL': settings.STATUS_AWAITING_APPROVAL,
        'STATUS_READY_TO_EXCHANGE': settings.STATUS_READY_TO_EXCHANGE,
        'STATUS_FINISHED': settings.STATUS_FINISHED,
        'STATUS_DELETED': settings.STATUS_DELETED,
        'input_offer': {
            'lat': request.session['input_offer']['lat'],
            'lng': request.session['input_offer']['lng'],
            'address': request.session['input_offer']['address'],
            'radius': request.session['input_offer']['radius'],
            'amount_from': request.session['input_offer']['amount_from'],
            'amount_to': request.session['input_offer']['amount_to'],
            'currency_from': request.session['input_offer']['currency_from'],
            'currency_to': request.session['input_offer']['currency_to'],
            'sort': request.session['input_offer']['sort'],
        },
        'show_cookies': not bool(request.COOKIES.get('cookies-allowed')),
        'notifications': len(get_offers_waiting_for_user_reaction(marek))
    }
