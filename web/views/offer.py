from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models.query_utils import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic.base import View

from web.forms import OfferSearchForm, OfferForm, FeedbackForm
from web.models import Offer, Currency
from web.service.acl import can_user_access_offer
from web.service.offer import get_minimum_amount_for_currencies, get_maximum_amount_for_currencies, get_sorted_offers, \
    get_offer_visible_feedbacks, create_feedback, create_offer
from web.service import offer_sorting_strategies
from web.service.user import get_user_feedbacks
from web.templatetags.web_extras import get_other_user


class ListView(View):
    def get(self, request):
        input_offer = request.session['input_offer']
        minimal_amount = get_minimum_amount_for_currencies(input_offer['currency_to'], input_offer['currency_from'])
        maximal_amount = get_maximum_amount_for_currencies(input_offer['currency_to'], input_offer['currency_from'])

        form = OfferSearchForm(initial=input_offer)
        form.fields['currency_to'].queryset = form.fields['currency_to'].queryset.filter(
            ~Q(pk=input_offer['currency_from'])
        )
        offers = get_sorted_offers(
            input_offer=request.session['input_offer'],
            sorting_strategy=self.get_sorting_strategy(input_offer['sort']),
            currency_from=input_offer['currency_from'],
            currency_to=input_offer['currency_to'],
            amount_from=input_offer['amount_from'],
            amount_to=input_offer['amount_to'],
            user=request.user
        )

        context = {
            'offers': offers,
            'form': form,
            'currency_minimum': minimal_amount,
            'currency_maximum': maximal_amount
        }

        template = "web/offer/list-ajax.html" if request.is_ajax() else "web/offer/list.html"

        return render(request, template, context)

    def post(self, request):
        amount_from = int(request.POST.get('amount_from'))
        amount_to = int(request.POST.get('amount_to'))
        currency_from = int(request.POST.get('currency_from'))
        currency_to = int(request.POST.get('currency_to'))
        input_offer = request.session['input_offer']

        input_offer['amount_from'] = amount_from
        input_offer['amount_to'] = amount_to

        if input_offer['currency_from'] != currency_from or input_offer['currency_to'] != currency_to:
            input_offer['amount_from'] = get_minimum_amount_for_currencies(currency_to, currency_from)
            input_offer['amount_to'] = get_maximum_amount_for_currencies(currency_to, currency_from)

        input_offer['currency_from'] = currency_from
        input_offer['currency_to'] = currency_to

        request.session.modified = True
        return redirect('offer_list')

    @staticmethod
    def get_sorting_strategy(identificator):
        if identificator == 'amount':
            return offer_sorting_strategies.AmountSortingStrategy()
        elif identificator == 'stars':
            return offer_sorting_strategies.StarsSortingStrategy()
        elif identificator == 'distance':
            return offer_sorting_strategies.DistanceSortingStrategy()
        else:
            return offer_sorting_strategies.RatingsSortingStrategy()


class SortView(View):
    @staticmethod
    def get(request, sort):
        request.session['input_offer']['sort'] = sort
        request.session.modified = True
        return redirect('offer_list')


class DetailView(View):
    @staticmethod
    def get(request, id):
        offer = get_object_or_404(Offer, pk=id)

        if not can_user_access_offer(request.user, offer):
            messages.add_message(request, messages.INFO, _('You do not have permission.'))
            return redirect('offer_list')

        form = FeedbackForm(initial={'amount_to': 0})

        context = {
            'offer': offer,
            'feedback_form': form,
            'has_feedback': offer.has_users_feedback(request.user),
            'feedbacks': get_user_feedbacks(offer.user_created),
            'other_user': get_other_user(offer, request.user),
            'visible_feedbacks': get_offer_visible_feedbacks(offer)
        }

        template = "web/offer/detail-ajax.html" if request.is_ajax() else "web/offer/detail.html"

        return render(request, template, context)


class FeedbackView(View):
    @staticmethod
    def post(request, id):
        create_feedback(
            offer=Offer.objects.get(pk=id),
            user=request.user,
            comment=request.POST.get('comment'),
            stars=int(request.POST.get('stars')),
        )
        messages.add_message(request, messages.INFO, _('Feedback was added.'))
        return redirect('offer_detail', id=id)


@method_decorator(login_required, name='dispatch')
class NewView(View):
    template_name = "web/offer/new.html"

    def post(self, request):
        currency_from = Currency.objects.get(pk=int(request.POST.get('currency_from')))
        currency_to = Currency.objects.get(pk=int(request.POST.get('currency_to')))
        create_offer(
            lat=float(request.POST.get('lat')),
            lng=float(request.POST.get('lng')),
            radius=int(request.POST.get('radius')),
            amount=int(request.POST.get('amount_from')),
            comment=request.POST.get('comment'),
            currency_from=currency_from,
            currency_to=currency_to,
            user_created=request.user,
            address=request.POST.get('address'),
        )
        messages.add_message(request, messages.INFO, _('Offer was added.'))
        return redirect('offer_new')

    def get(self, request):
        form = OfferForm(initial={'amount_to': 0, 'currency_from': 1, 'currency_to': 2})
        return render(request, "web/offer/new.html", {'form': form})
