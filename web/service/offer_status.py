from django.core.exceptions import PermissionDenied

from dip import settings
from web.service.mail import send_mail


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
    send_mail(
        folder='created',
        file='awaiting_approval',
        to_email=offer.user_created.userprofile.email,
        subject='TOOD subject',
        context={}
    )


def approve(offer, user):
    if offer.status.id != settings.STATUS_AWAITING_APPROVAL:
        raise PermissionDenied
    if user != offer.user_created:
        raise PermissionDenied

    offer.status_id = settings.STATUS_READY_TO_EXCHANGE
    offer.save()
    send_mail(
        folder='responded',
        file='approved',
        to_email=offer.user_responded.userprofile.email,
        subject='TOOD subject',
        context={}
    )


def refuse(offer, user):
    if offer.status.id != settings.STATUS_AWAITING_APPROVAL:
        raise PermissionDenied
    if user != offer.user_created:
        raise PermissionDenied

    send_mail(
        folder='responded',
        file='not_approved',
        to_email=offer.user_responded.userprofile.email,
        subject='TOOD subject',
        context={}
    )
    offer.status_id = settings.STATUS_AWAITING_ACCEPTANCE
    offer.user_responded = None
    offer.save()


def already_not_interested(offer, user):
    if offer.status.id != settings.STATUS_AWAITING_APPROVAL:
        raise PermissionDenied
    if user != offer.user_responded:
        raise PermissionDenied

    send_mail(
        folder='created',
        file='already_not_awaiting_approval',
        to_email=offer.user_created.userprofile.email,
        subject='TOOD subject',
        context={}
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
        send_mail(
            folder='responded',
            file='already_not_rte',
            to_email=offer.user_responded.userprofile.email,
            subject='TOOD subject',
            context={}
        )
    else:
        send_mail(
            folder='created',
            file='already_not_rte',
            to_email=offer.user_created.userprofile.email,
            subject='TOOD subject',
            context={}
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
        send_mail(
            folder='both',
            file='finished',
            to_email=offer.user_responded.userprofile.email,
            subject='TOOD subject',
            context={}
        )
    else:
        send_mail(
            folder='both',
            file='finished',
            to_email=offer.user_created.userprofile.email,
            subject='TOOD subject',
            context={}
        )
