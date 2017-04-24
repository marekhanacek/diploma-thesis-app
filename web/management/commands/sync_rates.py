import urllib
import json
from django.core.management.base import BaseCommand

from web.models import Currency, CurrencyRates


class Command(BaseCommand):
    help = 'Synchronizes currency rates'

    def handle(self, *args, **options):
        currencies = self.get_currencies()
        for currency_from in currencies.values():
            rates = self.get_rates(currency_from.identificator, currencies.keys())
            for identificator, rate in rates.items():
                currency_to = currencies[identificator]
                CurrencyRates.objects.update_or_create(
                    currency_from=currency_from,
                    currency_to=currency_to,
                    defaults={'rate': rate}
                )

    @staticmethod
    def get_currencies():
        currencies = {}
        for currency in Currency.objects.all():
            currencies[currency.identificator] = currency
        return currencies

    def get_rates(self, base, symbols):
        req = urllib.request.urlopen(self.get_url(base, symbols))
        content = json.loads(req.read().decode("utf-8"))
        return content['rates']

    @staticmethod
    def get_url(base, symbols):
            return 'http://api.fixer.io/latest?symbols=' + ','.join(symbols) + '&base=' + base
