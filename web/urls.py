from rest_framework import routers
from django.conf.urls import url, include
from rest_framework.documentation import include_docs_urls

from web.views import other
from web.views.api import OfferViewSet, CurrencyViewSet, UserViewSet, LanguageViewSet, login
from .views import offer, page, sign, user, offer_status

router = routers.DefaultRouter()
router.register(r'offer', OfferViewSet)
router.register(r'currency', CurrencyViewSet)
router.register(r'user', UserViewSet)
router.register(r'language', LanguageViewSet)

urlpatterns = [
    url(r'^$', offer.ListView.as_view(), name='offer_list'),
    url(r'^offer/sort/(.*)$', offer.SortView.as_view(), name='offer_sort'),
    url(r'^offer/detail/(?P<id>[0-9]+)$', offer.DetailView.as_view(), name='offer_detail'),
    url(r'^feedback/(?P<id>[0-9]+)$', offer.FeedbackView.as_view(), name='feedback'),
    url(r'^offer/new$', offer.NewView.as_view(), name='offer_new'),

    # states
    url(r'^offer/delete/(?P<id>[0-9]+)$', offer_status.DeleteView.as_view(), name='offer_delete'),
    url(r'^offer/accept/(?P<id>[0-9]+)$', offer_status.AcceptView.as_view(), name='offer_accept'),
    url(r'^offer/approve/(?P<id>[0-9]+)$', offer_status.ApproveView.as_view(), name='offer_approve'),
    url(r'^offer/refuse/(?P<id>[0-9]+)$', offer_status.RefuseView.as_view(), name='offer_refuse'),
    url(r'^offer/already-not-interested/(?P<id>[0-9]+)$', offer_status.AlreadyNotInterestedView.as_view(), name='offer_already_not_interested'),
    url(r'^offer/offer-again/(?P<id>[0-9]+)$', offer_status.OfferAgainView.as_view(), name='offer_offer_again'),
    url(r'^offer/complete/(?P<id>[0-9]+)$', offer_status.CompleteView.as_view(), name='offer_complete'),

    url(r'^user-profile', user.ProfileView.as_view(), name='user_profile'),
    url(r'^user/(?P<id>[0-9]+)$', user.DetailView.as_view(), name='user_detail'),
    url(r'^change-location', user.ChangeLocationView.as_view(), name='change_location'),
    url(r'^user/change-preferences', user.ChangePreferencesView.as_view(), name='change_preferences'),
    url(r'^access-denied', user.AccessDeniedView.as_view(), name='access_denied'),

    url(r'^page/(.*)$', page.DetailView.as_view(), name='page'),

    url(r'^exchange-rate/(?P<currecy_from>[0-9]+)/(?P<currecy_to>[0-9]+)$', other.RateView.as_view(), name='exchange_rate'),

    url(r'^logout$', sign.LogoutView.as_view(), name='logout'),

    url(r'^api/', include(router.urls)),
    url(r'^api/docs/', include_docs_urls(title='My API title'))
]
