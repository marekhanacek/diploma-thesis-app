from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import logout as auth_logout
from django.utils.decorators import method_decorator
from django.views.generic.base import View


@method_decorator(login_required, name='dispatch')
class LogoutView(View):
    @staticmethod
    def get(request):
        auth_logout(request)
        return redirect('offer_list')