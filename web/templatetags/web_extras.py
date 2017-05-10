from django import template
from django.utils.formats import number_format
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

from web.models import Currency
from web.service import offer as offer_service
from web.service.user import is_verified

register = template.Library()


@register.filter
def format_offer_currency_from(offer):
    return offer.currency_from_formatted()


@register.filter
def format_offer_currency_to(offer):
    return offer.currency_to_formatted()


@register.filter(is_safe=True)
def print_verified(user):
    if is_verified(user):
        return mark_safe(
            '<span'
            ' class="glyphicon glyphicon-ok glyphicon-verified img-circle"'
            ' data-toggle="tooltip"'
            ' data-placement="top"'
            ' title="'+_("User is verified")+'"'
            '>'
            '</span>')
    else:
        return ''


@register.filter(is_safe=True)
def print_stars(stars):
    return mark_safe('<span class="glyphicon glyphicon-star icon-my-star"></span> ' * stars)


@register.filter
def is_feedback_visible(feedback):
    return offer_service.is_feedback_visible(feedback)


@register.assignment_tag
def is_user_verified(user):
    return is_verified(user)


@register.assignment_tag
def get_other_user(offer, user):
    if offer.user_created.id == user.id:
        return offer.user_responded
    else:
        return offer.user_created


@register.assignment_tag
def get_offer_distance_from(offer, lat, lng):
    return offer_service.get_offer_distance_from(offer, lat, lng)


@register.assignment_tag
def format_price(amount, currency_id):
    currency = Currency.objects.get(pk=currency_id)
    return currency.prefix + '<span class="amount">' + number_format(amount, 0) + '</span>' + currency.postfix
