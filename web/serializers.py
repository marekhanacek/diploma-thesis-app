from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from web.models import Offer, Currency, Feedback, Language, UserProfile
from web.service.offer import create_offer
from web.service.user import is_verified, get_user_stars


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = (
            'id',
            'currency_from',
            'currency_to',
            'status',
            'user_created',
            'user_responded',
            'address',
            'radius',
            'lat',
            'lng',
            'amount',
            'exchange_rate',
            'comment',
            'created_at',
            'updated_at'
        )
        read_only_fields = (
            'id',
            'user_created',
            'user_responded',
            'status',
            'created_at',
            'updated_at',
            'exchange_rate',
        )

    def create(self, validated_data):
        try:
            return create_offer(
                lat=validated_data.get('lat'),
                lng=validated_data.get('lng'),
                radius=validated_data.get('radius'),
                amount=validated_data.get('amount'),
                comment=validated_data.get('comment'),
                currency_from=validated_data.get('currency_from'),
                currency_to=validated_data.get('currency_to'),
                address=validated_data.get('address'),
                user_created=User.objects.get(pk=100),
            )
        except Exception as e:
            raise ValidationError(e)


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = (
            'id',
            'name',
            'identificator'
        )


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = (
            'id',
            'offer',
            'user_created',
            'comment',
            'stars',
            'created_at',
        )


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = (
            'id',
            'identificator',
            'name',
        )


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            'id',
            'user',
            'profile_photo',
            'home_currency',
            'exchange_currency',
            'language',
            'basic_information',
            'email',
            'phone',
            'address',
            'radius',
            'lat',
            'lng',
        )


class UserSerializer(serializers.ModelSerializer):
    userprofile = UserProfileSerializer()
    is_verified = serializers.SerializerMethodField()
    stars = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'is_verified',
            'stars',
            'email',
            'userprofile',
        )

    @staticmethod
    def get_is_verified(user):
        return is_verified(user)

    @staticmethod
    def get_stars(user):
        return get_user_stars(user)
