from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from django.test import TestCase

from dip import settings
from web.models import Offer


class BaseTestCase(TestCase):
    @staticmethod
    def get_offer_awaiting_acceptance():
        return Offer.objects.filter(status=settings.STATUS_AWAITING_ACCEPTANCE).first()

    @staticmethod
    def get_offer_awaiting_approval():
        return Offer.objects.filter(status=settings.STATUS_AWAITING_APPROVAL).first()

    @staticmethod
    def get_offer_ready_to_exchange():
        return Offer.objects.filter(status=settings.STATUS_READY_TO_EXCHANGE).first()

    @staticmethod
    def get_offer_finished():
        return Offer.objects.filter(status=settings.STATUS_FINISHED).first()

    @staticmethod
    def get_offer_deleted():
        return Offer.objects.filter(status=settings.STATUS_DELETED).first()

    @staticmethod
    def get_user_except(except_users=[]):
        query = User.objects
        for u in except_users:
            if u:
                query = query.filter(~Q(id=u.id))
        return query.first()

    @staticmethod
    def get_verified_user():
        return User.objects.filter(pk=2).first()

    @staticmethod
    def get_unverified_user():
        return User.objects.filter(pk=1).first()
