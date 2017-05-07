from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponse, Http404
from django.views.generic.base import View

from web.service.offer import get_exchange_rate


class RateView(View):
    @staticmethod
    def get(request, currecy_from, currecy_to):
        try:
            return HttpResponse(get_exchange_rate(currecy_from, currecy_to))
        except ObjectDoesNotExist:
            raise Http404
