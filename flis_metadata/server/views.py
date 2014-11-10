from django.core.urlresolvers import reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic import UpdateView

from flis_metadata.common import models
from flis_metadata.server.forms import EnableDisableForm
from flis_metadata.server.forms import CountryEditForm


class EnableDisableView(SuccessMessageMixin,
                        UpdateView):
    form_class = EnableDisableForm


class HomeView(TemplateView):
    template_name = 'home.html'


class GeographicalScopesView(ListView):
    model = models.GeographicalScope
    template_name = 'geographical_scopes.html'


class GeographicalScopesAddView(SuccessMessageMixin,
                                CreateView):
    model = models.GeographicalScope
    template_name = 'geographical_scopes_edit.html'
    success_message = 'Scope added successfully'

    def get_success_url(self):
        return reverse('geographical_scopes')


class GeographicalScopesEditView(SuccessMessageMixin,
                                 UpdateView):

    model = models.GeographicalScope
    template_name = 'geographical_scopes_edit.html'
    success_message = 'Scope updated successfully'

    def get_success_url(self):
        return reverse('geographical_scopes')


class GeographicalScopesEnableDisableView(EnableDisableView):
    model = models.GeographicalScope
    success_message = 'Scope updated successfully'

    def get_success_url(self):
        return reverse('geographical_scopes')


class EnvironmentalThemesView(ListView):
    model = models.EnvironmentalTheme
    template_name = 'environmental_themes.html'


class EnvironmentalThemesAddView(SuccessMessageMixin,
                                 CreateView):
    model = models.EnvironmentalTheme
    template_name = 'environmental_themes_edit.html'
    success_message = 'Theme added successfully'

    def get_success_url(self):
        return reverse('environmental_themes')


class EnvironmentalThemeEditView(SuccessMessageMixin,
                                 UpdateView):

    model = models.EnvironmentalTheme
    template_name = 'environmental_themes_edit.html'
    success_message = 'Theme updated successfully'

    def get_success_url(self):
        return reverse('environmental_themes')


class EnvironmentalThemeEnableDisableView(EnableDisableView):
    model = models.EnvironmentalTheme
    success_message = 'Theme updated successfully'

    def get_success_url(self):
        return reverse('environmental_themes')


class CountriesView(ListView):
    model = models.Country
    template_name = 'countries.html'


class CountriesAddView(SuccessMessageMixin,
                       CreateView):
    model = models.Country
    template_name = 'countries_edit.html'
    success_message = 'Country added successfully'

    def get_success_url(self):
        return reverse('countries')


class CountryEditView(SuccessMessageMixin,
                      UpdateView):

    model = models.Country
    template_name = 'countries_edit.html'
    success_message = 'Country updated successfully'
    form_class = CountryEditForm

    def get_success_url(self):
        return reverse('countries')


class CountryEnableDisableView(EnableDisableView):
    model = models.Country
    success_message = 'Country updated successfully'

    def get_success_url(self):
        return reverse('countries')
