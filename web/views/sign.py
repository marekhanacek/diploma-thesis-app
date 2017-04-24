from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth import logout as auth_logout, login as auth_login
from django.utils.decorators import method_decorator
from django.views.generic.base import View

from dip.settings import AUTHENTICATION_BACKENDS
from dip.settings_local import DEBUG


@method_decorator(login_required, name='dispatch')
class LogoutView(View):
    @staticmethod
    def get(request):
        auth_logout(request)
        return redirect('offer_list')


class LoginView(View):
    @staticmethod
    def get(request, id):
        if DEBUG:
            db_user = User.objects.get(pk=id)
            db_user.backend = AUTHENTICATION_BACKENDS[0]
            auth_login(request, db_user)
        return redirect('offer_list')