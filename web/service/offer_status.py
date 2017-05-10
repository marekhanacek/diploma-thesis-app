from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext as _

from dip import settings
from web.service.mail import send_offer_mail


def delete(offer, user):
    if offer.status.id != settings.STATUS_AWAITING_ACCEPTANCE:
        raise PermissionDenied
    if user != offer.user_created:
        raise PermissionDenied

    offer.status_id = settings.STATUS_DELETED
    offer.save()


def accept(offer, user):
    if offer.status.id != settings.STATUS_AWAITING_ACCEPTANCE:
        raise PermissionDenied
    if user == offer.user_created:
        raise PermissionDenied

    offer.status_id = settings.STATUS_AWAITING_APPROVAL
    offer.user_responded = user
    offer.save()

    send_offer_mail(
        folder='created',
        file='awaiting_approval',
        subject=_('Offer was accepted'),
        offer=offer,
        user=offer.user_created,
        other_user=user
    )


def approve(offer, user):
    if offer.status.id != settings.STATUS_AWAITING_APPROVAL:
        raise PermissionDenied
    if user != offer.user_created:
        raise PermissionDenied

    offer.status_id = settings.STATUS_READY_TO_EXCHANGE
    offer.save()

    send_offer_mail(
        folder='responded',
        file='approved',
        subject=_('You were approved in offer'),
        offer=offer,
        user=offer.user_responded,
        other_user=user
    )


def refuse(offer, user):
    if offer.status.id != settings.STATUS_AWAITING_APPROVAL:
        raise PermissionDenied
    if user != offer.user_created:
        raise PermissionDenied

    send_offer_mail(
        folder='responded',
        file='not_approved',
        subject=_('You were not approved in offer'),
        offer=offer,
        user=offer.user_responded,
        other_user=user
    )

    offer.status_id = settings.STATUS_AWAITING_ACCEPTANCE
    offer.user_responded = None
    offer.save()


def already_not_interested(offer, user):
    if offer.status.id != settings.STATUS_AWAITING_APPROVAL:
        raise PermissionDenied
    if user != offer.user_responded:
        raise PermissionDenied

    send_offer_mail(
        folder='created',
        file='already_not_awaiting_approval',
        subject=_('User is already not interested in offer'),
        offer=offer,
        user=offer.user_created,
        other_user=user
    )

    offer.status_id = settings.STATUS_AWAITING_ACCEPTANCE
    offer.user_responded = None
    offer.save()


def offer_again(offer, user):
    if offer.status.id != settings.STATUS_READY_TO_EXCHANGE:
        raise PermissionDenied
    if user != offer.user_created and user != offer.user_responded:
        raise PermissionDenied

    if user.id == offer.user_created.id:
        send_offer_mail(
            folder='responded',
            file='already_not_rte',
            subject=_('Offer was canceled'),
            offer=offer,
            user=offer.user_responded,
            other_user=user
        )
    else:
        send_offer_mail(
            folder='created',
            file='already_not_rte',
            subject=_('Offer is awailable for other users'),
            offer=offer,
            user=offer.user_created,
            other_user=user
        )

    offer.status_id = settings.STATUS_AWAITING_ACCEPTANCE
    offer.user_responded = None
    offer.save()


def complete(offer, user):
    if offer.status.id != settings.STATUS_READY_TO_EXCHANGE:
        raise PermissionDenied
    if user != offer.user_created and user != offer.user_responded:
        raise PermissionDenied

    offer.status_id = settings.STATUS_FINISHED
    offer.save()

    if user.id == offer.user_created.id:
        send_offer_mail(
            folder='both',
            file='finished',
            subject=_('Offer is complete'),
            offer=offer,
            user=offer.user_responded,
            other_user=user
        )
    else:
        send_offer_mail(
            folder='both',
            file='finished',
            subject=_('Offer is complete'),
            offer=offer,
            user=offer.user_created,
            other_user=user
        )
