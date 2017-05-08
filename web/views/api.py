from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.decorators import detail_route, list_route
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from django.contrib.auth import login
from django.http.response import HttpResponse
from social_django.utils import psa
from rest_framework.authtoken.models import Token
from rest_framework import mixins

from web.models import Offer, Currency, Language
from web.serializers import OfferSerializer, CurrencySerializer, FeedbackSerializer, UserSerializer, \
    LanguageSerializer
from web.service.api_permission import IsActualUserLogged, CanUserAccessOffer
from web.service.offer import get_sorted_offers, get_offer_visible_feedbacks, create_feedback, get_finished_offers, \
    get_offers_waiting_for_other_user_reaction, get_offers_waiting_for_user_reaction
from web.service.offer_sorting_strategies import AmountSortingStrategy
from web.service import offer_status
from web.service.user import get_user_feedbacks


class OfferViewSet(viewsets.ReadOnlyModelViewSet, mixins.CreateModelMixin):
    """
    list:
    Return a list of all offers by parameters -- currency_from, currency_to, amount_from, amount_to, lat, lng and radius.

    retrieve:
    Return the given offer.

    create:
    Create a new offer instance.

    partial_update:
    Partial update of status by action parameter.
    """
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer

    def list(self, request, currency_from, currency_to, *args, **kwargs):
        queryset = self.filter_queryset(self.get_my_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_my_queryset(self):
        currency_from = self.request.query_params.get('currency_from', None)
        currency_to = self.request.query_params.get('currency_to', None)
        amount_from = self.request.query_params.get('amount_from', None)
        amount_to = self.request.query_params.get('amount_to', None)
        lat = self.request.query_params.get('lat', None)
        lng = self.request.query_params.get('lng', None)
        radius = self.request.query_params.get('radius', None)

        if not currency_from:
            raise ParseError('Required parameter currency_from is missing.')
        if not currency_to:
            raise ParseError('Required parameter currency_to is missing.')
        if not lat:
            raise ParseError('Required parameter lat is missing.')
        if not lng:
            raise ParseError('Required parameter lng is missing.')
        if not radius:
            raise ParseError('Required parameter radius is missing.')

        return get_sorted_offers(
            input_offer={
                'lat': lat,
                'lng': lng,
                'radius': radius,
            },
            sorting_strategy=AmountSortingStrategy(),
            currency_from=currency_from,
            currency_to=currency_to,
            amount_from=amount_from,
            amount_to=amount_to
        )

    def partial_update(self, request, *args, **kwargs):
        action = self.request.data['action']
        if action == 'delete':
            offer_status.delete(self.get_object(), request.user)
        if action == 'accept':
            offer_status.accept(self.get_object(), request.user)
        if action == 'approve':
            offer_status.approve(self.get_object(), request.user)
        if action == 'refuse':
            offer_status.refuse(self.get_object(), request.user)
        if action == 'already_not_interested':
            offer_status.already_not_interested(self.get_object(), request.user)
        if action == 'offer_again':
            offer_status.offer_again(self.get_object(), request.user)
        if action == 'complete':
            offer_status.complete(self.get_object(), request.user)
        else:
            raise ParseError('Unknown action')
        return Response(OfferSerializer(self.get_object()).data)

    @detail_route(methods=['get', 'post'], permission_classes=[CanUserAccessOffer])
    def feedback(self, request, *args, **kwargs):
        if request.method == 'POST':
            create_feedback(
                offer=self.get_object(),
                user=request.user,
                comment=self.request.query_params.get('comment'),
                stars=self.request.query_params.get('stars')
            )
            return Response(
                FeedbackSerializer(get_offer_visible_feedbacks(self.get_object()), many=True).data,
                status=status.HTTP_201_CREATED
            )

        elif request.method == 'GET':
            return Response(FeedbackSerializer(get_offer_visible_feedbacks(self.get_object()), many=True).data)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    list:
    Return a list of all the existing users.

    retrieve:
    Return the given user.

    create:
    Create a new user instance.

    feedback:
    Return user's feedbacks.

    finished_offers:
    Return all user's finished offer.

    user_reaction:
    Return all offers that are waiting for user reaction.

    other_user_reaction:
    Return all offers that are waiting for other user reaction.

    login:
    Login user.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @detail_route(methods=['get'])
    def feedback(self, *args, **kwargs):
        return Response(
            FeedbackSerializer(get_user_feedbacks(self.get_object()), many=True).data
        )

    @detail_route(methods=['get'], permission_classes=[IsActualUserLogged])
    def finished_offers(self, *args, **kwargs):
        return Response(
            OfferSerializer(get_finished_offers(self.get_object()), many=True).data
        )

    @detail_route(methods=['get'], permission_classes=[IsActualUserLogged])
    def user_reaction(self, *args, **kwargs):
        return Response(
            OfferSerializer(get_offers_waiting_for_user_reaction(self.get_object()), many=True).data
        )

    @detail_route(methods=['get'], permission_classes=[IsActualUserLogged])
    def other_user_reaction(self, *args, **kwargs):
        return Response(
            OfferSerializer(get_offers_waiting_for_other_user_reaction(self.get_object()), many=True).data
        )

    @psa('social:complete')
    @list_route(methods=['get'], permission_classes=[IsActualUserLogged])
    def login(self, request, backend, *args, **kwargs):
        try:
            user = request.backend.do_auth(request.GET.get('access_token'))
        except AttributeError:
            raise ParseError('Required parameter access_token is missing.')

        if user:
            login(request, user)
            token = Token.objects.create(user=user)
            return HttpResponse(token.key)
        else:
            return HttpResponse('ERROR')


class CurrencyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
    Return the given currency.

    list:
    Return a list of all the existing currencies.
    """
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


class LanguageViewSet(viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
    Return the given language.

    list:
    Return a list of all the existing languages.
    """
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
