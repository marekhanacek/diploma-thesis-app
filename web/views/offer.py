from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db.models.query_utils import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic.base import View, TemplateView

from web.forms import OfferSearchForm, OfferForm, FeedbackForm
from web.models import Offer
from web.service.acl import can_user_access_offer
from web.service.offer import get_sorted_offers, \
    get_offer_feedback_user_created, get_offer_feedback_user_responded, get_minimum_amount_for_offers, \
    get_maximum_amount_for_offers
from web.service.offer_sorting_strategies import get_sorting_strategy_by_identificator
from web.service.user import get_user_feedbacks, get_user_stars
from web.templatetags.web_extras import get_other_user


class ListView(TemplateView):
    def get_template_names(self):
        return ["web/offer/list-ajax.html" if self.request.is_ajax() else "web/offer/list.html"]

    def get_context_data(self, **kwargs):
        input_offer = self.request.session['input_offer']
        form = OfferSearchForm(initial=input_offer)
        form.fields['currency_to'].queryset = form.fields['currency_to'].queryset.filter(
            ~Q(pk=input_offer['currency_from'])
        )
        offers = get_sorted_offers(
            input_offer=self.request.session['input_offer'],
            sorting_strategy=get_sorting_strategy_by_identificator(input_offer['sort']),
            currency_from=input_offer['currency_from'],
            currency_to=input_offer['currency_to'],
            user=self.request.user
        )
        return {
            'offers': get_sorted_offers(
                input_offer=self.request.session['input_offer'],
                sorting_strategy=get_sorting_strategy_by_identificator(input_offer['sort']),
                currency_from=input_offer['currency_from'],
                currency_to=input_offer['currency_to'],
                amount_from=input_offer['amount_from'],
                amount_to=input_offer['amount_to'],
                user=self.request.user
            ),
            'form': form,
            'currency_minimum': get_minimum_amount_for_offers(offers),
            'currency_maximum': get_maximum_amount_for_offers(offers)
        }

    def post(self, request):
        form = OfferSearchForm(request.POST)
        if form.is_valid():
            form.process(request)
        return redirect('offer_list')


class SortView(View):
    @staticmethod
    def get(request, sort):
        request.session['input_offer']['sort'] = sort
        request.session.modified = True
        return redirect('offer_list')


class DetailView(TemplateView):
    def get(self, request, *args, **kwargs):
        offer = get_object_or_404(Offer, pk=int(kwargs['id']))
        if not can_user_access_offer(request.user, offer):
            messages.add_message(request, messages.INFO, _('Access denied. You do not have permission.'))
            return redirect('offer_list')
        return super().get(self, request, *args, **kwargs)

    def get_context_data(self, id, **kwargs):
        offer = get_object_or_404(Offer, pk=id)
        other_user = get_other_user(offer, self.request.user)
        context = {
            'offer': offer,
            'feedback_form': FeedbackForm(initial={'amount_to': 0}),
            'other_user': other_user,
            'stars': get_user_stars(
                other_user if other_user
                else offer.user_created
            ),
            'feedbacks': get_user_feedbacks(
                other_user if other_user
                else offer.user_created
            )
        }
        if offer.status.is_finished():
            context['user_feedback'] = get_offer_feedback_user_created(offer, self.request.user)
            context['other_user_feedback'] = get_offer_feedback_user_responded(offer, self.request.user)
        return context

    def get_template_names(self):
        return ["web/offer/detail-ajax.html" if self.request.is_ajax() else "web/offer/detail.html"]


class FeedbackView(View):
    @staticmethod
    def post(request, id):
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.process(id, request.user)
            messages.add_message(request, messages.INFO, _('Feedback was added.'))
        else:
            messages.add_message(request, messages.INFO, _('Feedback process ERROR.'))
        return redirect('offer_detail', id=id)


@method_decorator(login_required, name='dispatch')
class NewView(View):
    template_name = "web/offer/new.html"

    def get(self, request):
        profile = request.user.userprofile
        form = OfferForm(initial={
            'amount_to': 0,
            'currency_from': profile.home_currency,
            'currency_to': profile.exchange_currency,
            'lat': profile.lat,
            'lng': profile.lng,
            'address': profile.address,
            'radius': profile.radius,
        })
        return render(request, "web/offer/new.html", {'form': form})

    def post(self, request):
        form = OfferForm(request.POST)
        if form.is_valid():
            form.process(request.user)
            messages.add_message(request, messages.INFO, _('Offer was added.'))
        else:
            messages.add_message(request, messages.INFO, _('Offer process ERROR.'))
        return redirect('offer_new')
