from django.views.generic import ListView
from django.views.generic import TemplateView

from flis_metadata.common import models


class HomeView(TemplateView):
    template_name = 'home.html'


class GeographicalScopesView(ListView):
    model = models.GeographicalScope
    template_name = 'geographical_scopes.html'
