def template_variables(request):
    show_cookies = not bool(request.COOKIES.get('cookies-allowed'))
    return {
        'STATUS_AWAITING_ACCEPTANCE': 1,
        'STATUS_AWAITING_APPROVAL': 2,
        'STATUS_READY_TO_EXCHANGE': 3,
        'STATUS_FINISHED': 4,
        'STATUS_DELETED': 4,
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
        'show_cookies': show_cookies
    }
