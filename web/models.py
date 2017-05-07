from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.db import models

from dip import settings


class Currency(models.Model):
    name = models.CharField(max_length=50)
    identificator = models.CharField(max_length=3)
    prefix = models.CharField(max_length=5)
    postfix = models.CharField(max_length=5)

    def __str__(self):
        return self.identificator


class CurrencyRates(models.Model):
    currency_from = models.ForeignKey(Currency, on_delete=models.PROTECT, related_name='currency_rates_from')
    currency_to = models.ForeignKey(Currency, on_delete=models.PROTECT, related_name='currency_rates_to')
    rate = models.FloatField()


class OfferStatus(models.Model):
    title = models.CharField(max_length=30)

    def is_awaiting_acceptance(self):
        return self.id == settings.STATUS_AWAITING_ACCEPTANCE

    def is_awaiting_approval(self):
        return self.id == settings.STATUS_AWAITING_APPROVAL

    def is_ready_to_exchange(self):
        return self.id == settings.STATUS_READY_TO_EXCHANGE

    def is_finished(self):
        return self.id == settings.STATUS_FINISHED

    def is_deleted(self):
        return self.id == settings.STATUS_DELETED


class Offer(models.Model):
    currency_from = models.ForeignKey(Currency, on_delete=models.PROTECT, related_name='offers_from')
    currency_to = models.ForeignKey(Currency, on_delete=models.PROTECT, related_name='offers_to')
    status = models.ForeignKey(OfferStatus, on_delete=models.PROTECT)
    user_created = models.ForeignKey(User, on_delete=models.PROTECT, related_name='created_offers')
    user_responded = models.ForeignKey(User, on_delete=models.PROTECT, related_name='responded_offers', null=True)
    address = models.TextField(default='')
    radius = models.FloatField()
    lat = models.FloatField()
    lng = models.FloatField()
    amount = models.IntegerField()
    exchange_rate = models.FloatField()
    comment = models.TextField(default='')

    # dates
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    @property
    def get_total(self):
        return self.amount * self.exchange_rate

    def iterate_users(self):
        yield self.user_created
        yield self.user_responded

    def is_user_attached(self, user):
        return user == self.user_created or user == self.user_responded


class Feedback(models.Model):
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name='feedbacks')
    user_created = models.ForeignKey(User, on_delete=models.PROTECT, related_name='feedbacks_created')
    user_responded = models.ForeignKey(User, on_delete=models.PROTECT, related_name='feedbacks_responded')
    comment = models.TextField(default='')
    stars = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)


class Language(models.Model):
    identificator = models.CharField(max_length=10)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.identificator


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    profile_photo = models.ImageField(upload_to='uploads/profile_photos/', null=True)
    home_currency = models.ForeignKey(Currency, on_delete=models.PROTECT, related_name='profiles_having_home_currency',
                                      null=True)
    exchange_currency = models.ForeignKey(Currency, on_delete=models.PROTECT,
                                          related_name='profiles_having_exchange_currency', null=True)
    language = models.ForeignKey(Language, on_delete=models.PROTECT, related_name='profiles_having_language', null=True)
    basic_information = models.TextField(default='', blank=True)
    email = models.CharField(max_length=150, default='')
    phone = models.CharField(max_length=20, default='', blank=True)
    address = models.CharField(max_length=255, default='')
    radius = models.FloatField(default=0)
    lat = models.FloatField(default=0)
    lng = models.FloatField(default=0)

    @property
    def number_of_offers(self):
        return self.user.created_offers.count() + self.user.responded_offers.count()
