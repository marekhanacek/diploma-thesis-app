from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from django.contrib.auth import login
from django.http.response import HttpResponse
from social_django.utils import psa

from web.models import Offer, Currency, Language
from web.serializers import OfferSerializer, CurrencySerializer, FeedbackSerializer, UserSerializer, \
    LanguageSerializer
from web.service.offer import get_sorted_offers, get_offer_visible_feedbacks, create_feedback
from web.service.offer_sorting_strategies import AmountSortingStrategy
from web.service import offer_status


class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer

    def list(self, request, *args, **kwargs):
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

    @detail_route(methods=['post'])
    def delete(self, *args, **kwargs):
        offer = self.get_object()
        user = None
        offer_status.delete(offer, user)
        return Response(OfferSerializer(offer).data)

    @detail_route(methods=['post'])
    def accept(self, *args, **kwargs):
        offer = self.get_object()
        user = None
        offer_status.accept(offer, user)
        return Response(OfferSerializer(offer).data)

    @detail_route(methods=['post'])
    def approve(self, *args, **kwargs):
        offer = self.get_object()
        user = None
        offer_status.approve(offer, user)
        return Response(OfferSerializer(offer).data)

    @detail_route(methods=['post'])
    def refuse(self, *args, **kwargs):
        offer = self.get_object()
        user = None
        offer_status.refuse(offer, user)
        return Response(OfferSerializer(offer).data)

    @detail_route(methods=['post'])
    def already_not_interested(self, *args, **kwargs):
        offer = self.get_object()
        user = None
        offer_status.already_not_interested(offer, user)
        return Response(OfferSerializer(offer).data)

    @detail_route(methods=['post'])
    def offer_again(self, *args, **kwargs):
        offer = self.get_object()
        user = None
        offer_status.offer_again(offer, user)
        return Response(OfferSerializer(offer).data)

    @detail_route(methods=['post'])
    def complete(self, *args, **kwargs):
        offer = self.get_object()
        user = None
        offer_status.complete(offer, user)
        return Response(OfferSerializer(offer).data)

    @detail_route(methods=['get', 'post'])
    def feedback(self, request, pk, *args, **kwargs):
        if request.method == 'POST':
            offer = Offer.objects.get(pk=pk)
            user = User.objects.get(pk=100)
            create_feedback(
                offer=offer,
                user=user,
                comment=self.request.query_params.get('comment'),
                stars=self.request.query_params.get('stars')
            )
            return Response(FeedbackSerializer(get_offer_visible_feedbacks(offer), many=True).data)

        elif request.method == 'GET':
            offer = Offer.objects.get(pk=pk)
            return Response(FeedbackSerializer(get_offer_visible_feedbacks(offer), many=True).data)


class CurrencyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class LanguageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer


@psa('social:complete')
def register_by_access_token(request, backend):
    user = request.backend.do_auth(request.GET.get('access_token'))
    if user:
        login(request, user)
        return HttpResponse('OK')
    else:
        return HttpResponse('ERROR')
