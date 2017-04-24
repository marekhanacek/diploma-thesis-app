from django.http.response import Http404
from django.shortcuts import render
from django.views.generic.base import View
from django.template.loader import get_template
from django.template import TemplateDoesNotExist


class DetailView(View):
    def get(self, request, id):
        template_name = "web/page/" + id + ".html"
        try:
            get_template(template_name)
        except TemplateDoesNotExist:
            raise Http404
        return render(request, template_name)
