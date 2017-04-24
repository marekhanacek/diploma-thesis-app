from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic.base import View

from web.models import Offer
from web.service import offer_status


@method_decorator(login_required, name='dispatch')
class DeleteView(View):
    def post(self, request, id):
        offer = get_object_or_404(Offer, pk=id)
        offer_status.delete(offer, request.user)
        messages.add_message(request, messages.INFO, _('Offer was deleted.'))
        return redirect('offer_detail', id=id)


@method_decorator(login_required, name='dispatch')
class AcceptView(View):
    def post(self, request, id):
        offer = get_object_or_404(Offer, pk=id)
        offer_status.accept(offer, request.user)
        messages.add_message(request, messages.INFO, _('Offer was accepted.'))
        return redirect('offer_detail', id=id)


@method_decorator(login_required, name='dispatch')
class ApproveView(View):
    def post(self, request, id):
        offer = get_object_or_404(Offer, pk=id)
        offer_status.approve(offer, request.user)
        messages.add_message(request, messages.INFO, _('Offer was approved.'))
        return redirect('offer_detail', id=id)


@method_decorator(login_required, name='dispatch')
class RefuseView(View):
    def post(self, request, id):
        offer = get_object_or_404(Offer, pk=id)
        offer_status.refuse(offer, request.user)
        messages.add_message(
            request,
            messages.INFO,
            _('User was refused and offer is again available for other users.')
        )
        return redirect('offer_detail', id=id)


@method_decorator(login_required, name='dispatch')
class AlreadyNotInterestedView(View):
    def post(self, request, id):
        offer = get_object_or_404(Offer, pk=id)
        offer_status.already_not_interested(offer, request.user)
        messages.add_message(request, messages.INFO, _('You were deleted from this offer.'))
        return redirect('offer_detail', id=id)


@method_decorator(login_required, name='dispatch')
class OfferAgainView(View):
    def post(self, request, id):
        offer = get_object_or_404(Offer, pk=id)
        offer_status.offer_again(offer, request.user)

        if request.user.id == offer.user_created_id:
            messages.add_message(
                request,
                messages.INFO,
                _('Offer was canceled. Offer is again available for other users.')
            )
        else:
            messages.add_message(request, messages.INFO, _('Offer was canceled.'))
        return redirect('offer_detail', id=id)


@method_decorator(login_required, name='dispatch')
class CompleteView(View):
    def post(self, request, id):
        offer = get_object_or_404(Offer, pk=id)
        offer_status.complete(offer, request.user)
        messages.add_message(request, messages.INFO, _('Offer was marked as completed.'))
        return redirect('offer_detail', id=id)
