from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic.base import View, TemplateView

from web.forms import ChangePreferencesForm
from web.models import UserProfile
from web.service.offer import get_offers_waiting_for_user_reaction, get_offers_waiting_for_other_user_reaction, \
    get_finished_offers, get_history_of_users
from web.service.user import get_user_feedbacks, get_number_of_offers, save_user_location_to_session, get_user_stars


@method_decorator(login_required, name='dispatch')
class ProfileView(TemplateView):
    def get_template_names(self):
        return ["web/user/profile.html"]

    def get_context_data(self, **kwargs):
        return {
            'actual_offers_my': get_offers_waiting_for_user_reaction(self.request.user),
            'actual_offers_user': get_offers_waiting_for_other_user_reaction(self.request.user),
            'finished_offers': get_finished_offers(self.request.user),
            'stars': get_user_stars(self.request.user)
        }


class DetailView(TemplateView):
    def get(self, request, *args, **kwargs):
        id = int(kwargs['id'])
        if request.user.is_authenticated() and request.user.id == id and not request.is_ajax():
            return redirect('user_profile')
        return super().get(self, request, *args, **kwargs)

    def get_template_names(self):
        return ["web/user/detail-ajax.html" if self.request.is_ajax() else "web/user/detail.html"]

    def get_context_data(self, id, **kwargs):
        user = User.objects.get(pk=id)
        return {
            'actual_user': user,
            'history_with_user': get_history_of_users(user, self.request.user)
            if self.request.user.is_authenticated() else [],
            'feedbacks': get_user_feedbacks(user),
            'number_of_offers': get_number_of_offers(user),
            'stars': get_user_stars(user)
        }


class ChangeLocationView(View):
    def post(self, request):
        lat = float(request.POST.get('lat'))
        lng = float(request.POST.get('lng'))
        radius = int(request.POST.get('radius'))
        address = request.POST.get('address')

        save_user_location_to_session(
            session=request.session,
            lat=lat,
            lng=lng,
            radius=radius,
            address=address,
        )
        if request.user.is_authenticated():
            UserProfile.objects.update_or_create(
                user=request.user,
                defaults={
                    'radius': radius,
                    'lat': lat,
                    'lng': lng,
                    'address': address,
                }
            )
        return redirect('offer_list')


@method_decorator(login_required, name='dispatch')
class ChangePreferencesView(View):
    template_name = "web/user/change-preferences.html"

    def get(self, request):
        form = ChangePreferencesForm(instance=request.user.userprofile)
        return render(request, self.template_name, {'form': form})

    @staticmethod
    def post(request):
        form = ChangePreferencesForm(request.POST, instance=request.user.userprofile)
        if form.is_valid():
            form.process(request)
            messages.add_message(request, messages.INFO, _('Preferences were changed.'))
        else:
            messages.add_message(request, messages.INFO, _('ERROR'))
        return redirect('user_profile')


class AccessDeniedView(TemplateView):
    template_name = "web/user/access-denied.html"
