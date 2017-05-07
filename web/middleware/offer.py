from web.service.offer import get_sorted_offers, get_minimum_amount_for_offers, get_maximum_amount_for_offers
from web.service.offer_sorting_strategies import get_sorting_strategy_by_identificator


class OfferInSessionMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'input_offer' not in request.session:
            default_currency_from = 1
            default_currency_to = 2

            request.session['input_offer'] = {
                'lat': 50.0755381,
                'lng': 14.43780049999998,
                'address': 'Praha',
                'radius': 100,
                'amount_from': None,
                'amount_to': None,
                'currency_from': default_currency_from,
                'currency_to': default_currency_to,
                'sort': 'default',
            }

        input_offer = request.session['input_offer']
        if not input_offer['amount_from'] or not input_offer['amount_to']:
            offers = get_sorted_offers(
                input_offer=request.session['input_offer'],
                sorting_strategy=get_sorting_strategy_by_identificator(input_offer['sort']),
                currency_from=input_offer['currency_from'],
                currency_to=input_offer['currency_to'],
                user=request.user
            )
            input_offer['amount_from'] = get_minimum_amount_for_offers(offers)
            input_offer['amount_to'] = get_maximum_amount_for_offers(offers)
        request.session.modified = True
        response = self.get_response(request)
        return response
