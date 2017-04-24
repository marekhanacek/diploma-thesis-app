from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic.base import View

from web.forms import ChangePreferencesForm
from web.models import UserProfile
from web.service.language import change_language
from web.service.offer import get_offers_waiting_for_user_reaction, get_offers_waiting_for_other_user_reaction, \
    get_finished_offers, get_history_of_users
from web.service.user import get_user_feedbacks, get_number_of_offers, save_user_location_to_session, get_user_stars


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    @staticmethod
    def get(request):
        context = {
            'actual_offers_my': get_offers_waiting_for_user_reaction(request.user),
            'actual_offers_user': get_offers_waiting_for_other_user_reaction(request.user),
            'finished_offers': get_finished_offers(request.user),
            'stars': get_user_stars(request.user)
        }
        return render(request, "web/user/profile.html", context)


class DetailView(View):
    @staticmethod
    def get(request, id):
        id = int(id)
        if request.user.is_authenticated() and request.user.id == id and not request.is_ajax():
            return redirect('user_profile')

        actual_user = User.objects.get(pk=id)

        context = {
            'actual_user': actual_user,
            'history_with_user': get_history_of_users(actual_user, request.user) if request.user.is_authenticated()
            else [],
            'feedbacks': get_user_feedbacks(actual_user),
            'number_of_offers': get_number_of_offers(actual_user),
            'stars': get_user_stars(actual_user)
        }

        template = "web/user/detail-ajax.html" if request.is_ajax() else "web/user/detail.html"

        return render(request, template, context)


class ChangeLocationView(View):
    def post(self, request):
        save_user_location_to_session(
            session=request.session,
            lat=float(request.POST.get('lat')),
            lng=float(request.POST.get('lng')),
            radius=float(request.POST.get('radius')),
            address=request.POST.get('address'),
        )
        if request.user.is_authenticated():
            UserProfile.objects.update_or_create(
                user=request.user,
                defaults={
                    'radius': request.POST.get('radius'),
                    'lat': request.POST.get('lat'),
                    'lng': request.POST.get('lng'),
                    'address': request.POST.get('address'),
                }
            )
        return redirect('offer_list')


@method_decorator(login_required, name='dispatch')
class ChangePreferencesView(View):
    template_name = "web/user/change-preferences.html"

    def get(self, request):
        profile = request.user.userprofile
        form = ChangePreferencesForm(initial={
            'home_currency': profile.home_currency,
            'exchange_currency': profile.exchange_currency,
            'language': profile.language,
            'basic_information': profile.basic_information,
            'address': profile.address,
            'radius': profile.radius,
            'lat': profile.lat,
            'lng': profile.lng,
        })
        return render(request, self.template_name, {'form': form})

    @staticmethod
    def post(request):
        form = ChangePreferencesForm(request.POST)
        if form.is_valid():
            UserProfile.objects.update_or_create(
                user=request.user,
                defaults={
                    'home_currency': form.cleaned_data['home_currency'],
                    'exchange_currency': form.cleaned_data['exchange_currency'],
                    'language': form.cleaned_data['language'],
                    'basic_information': form.cleaned_data['basic_information'],
                    'address': form.cleaned_data['address'],
                    'radius': form.cleaned_data['radius'],
                    'lat': form.cleaned_data['lat'],
                    'lng': form.cleaned_data['lng']
                }
            )
            save_user_location_to_session(
                session=request.session,
                lat=float(form.cleaned_data['lat']),
                lng=float(form.cleaned_data['lng']),
                radius=float(form.cleaned_data['radius']),
                address=form.cleaned_data['address'],
            )
            language = form.cleaned_data['language']
            change_language(request, language.identificator)
            messages.add_message(request, messages.INFO, _('Preferences were changed.'))
        else:
            messages.add_message(request, messages.INFO, _('ERROR'))
        return redirect('user_profile')
