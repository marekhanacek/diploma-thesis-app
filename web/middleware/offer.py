from web.service.offer import get_minimum_amount_for_currencies, get_maximum_amount_for_currencies


class OfferInSessionMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'input_offer' not in request.session:
            default_currency_from = 1
            default_currency_to = 2
            default_amount_from = get_minimum_amount_for_currencies(default_currency_to, default_currency_from)
            default_amount_to = get_maximum_amount_for_currencies(default_currency_to, default_currency_from)

            request.session['input_offer'] = {
                'lat': 50.0755381,
                'lng': 14.43780049999998,
                'address': 'Praha',
                'radius': 100,
                'amount_from': default_amount_from,
                'amount_to': default_amount_to,
                'currency_from': default_currency_from,
                'currency_to': default_currency_to,
                'sort': 'default',
            }
        response = self.get_response(request)
        return response
