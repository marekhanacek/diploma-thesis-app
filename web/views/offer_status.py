from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic.base import View

from web.models import Offer
from web.service import offer_status


@method_decorator(login_required, name='dispatch')
class DeleteView(View):
    def post(self, request, id):
        try:
            offer_status.delete(get_object_or_404(Offer, pk=id), request.user)
            messages.add_message(request, messages.INFO, _('Offer was deleted.'))
        except PermissionDenied:
            messages.add_message(request, messages.INFO, _('Access denied.'))
        return redirect('offer_detail', id=id)


@method_decorator(login_required, name='dispatch')
class AcceptView(View):
    def post(self, request, id):
        try:
            offer_status.accept(get_object_or_404(Offer, pk=id), request.user)
            messages.add_message(request, messages.INFO, _('Offer was accepted.'))
        except PermissionDenied:
            messages.add_message(request, messages.INFO, _('Access denied.'))
        return redirect('offer_detail', id=id)


@method_decorator(login_required, name='dispatch')
class ApproveView(View):
    def post(self, request, id):
        try:
            offer_status.approve(get_object_or_404(Offer, pk=id), request.user)
            messages.add_message(request, messages.INFO, _('Offer was approved.'))
        except PermissionDenied:
            messages.add_message(request, messages.INFO, _('Access denied.'))
        return redirect('offer_detail', id=id)


@method_decorator(login_required, name='dispatch')
class RefuseView(View):
    def post(self, request, id):
        try:
            offer_status.refuse(get_object_or_404(Offer, pk=id), request.user)
            messages.add_message(
                request,
                messages.INFO,
                _('User was refused and offer is again available for other users.')
            )
        except PermissionDenied:
            messages.add_message(request, messages.INFO, _('Access denied.'))
        return redirect('offer_detail', id=id)


class AlreadyNotInterestedView(View):
    def post(self, request, id):
        try:
            offer_status.already_not_interested(get_object_or_404(Offer, pk=id), request.user)
            messages.add_message(request, messages.INFO, _('You were deleted from this offer.'))
        except PermissionDenied:
            messages.add_message(request, messages.INFO, _('Access denied.'))
        return redirect('offer_detail', id=id)


@method_decorator(login_required, name='dispatch')
class OfferAgainView(View):
    def post(self, request, id):
        try:
            offer = get_object_or_404(Offer, pk=id)
            offer_status.offer_again(offer, request.user)

            if request.user == offer.user_created:
                messages.add_message(
                    request,
                    messages.INFO,
                    _('Offer was canceled. Offer is again available for other users.')
                )
            else:
                messages.add_message(request, messages.INFO, _('Offer was canceled.'))
        except PermissionDenied:
            messages.add_message(request, messages.INFO, _('Access denied.'))
        return redirect('offer_detail', id=id)


@method_decorator(login_required, name='dispatch')
class CompleteView(View):
    def post(self, request, id):
        try:
            offer_status.complete(get_object_or_404(Offer, pk=id), request.user)
            messages.add_message(request, messages.INFO, _('Offer was marked as completed.'))
        except PermissionDenied:
            messages.add_message(request, messages.INFO, _('Access denied.'))
        return redirect('offer_detail', id=id)
