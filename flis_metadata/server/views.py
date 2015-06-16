from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic import UpdateView
from django.http import HttpResponse, Http404

from flis_metadata.common import models
from flis_metadata.server.forms import EnableDisableForm
from flis_metadata.server.forms import CountryEditForm


class AdminRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return render(request, 'restricted.html')
        if not request.user.has_perm('common.config'):
            return render(request, 'restricted.html')
        return super(AdminRequiredMixin, self).dispatch(request, *args,
                                                        **kwargs)


class MetadataEnableDisableView(AdminRequiredMixin,
                                SuccessMessageMixin,
                                UpdateView):
    form_class = EnableDisableForm


class MetadataCreateView(AdminRequiredMixin,
                         SuccessMessageMixin,
                         CreateView):
    pass


class MetadataUpdateView(AdminRequiredMixin,
                         SuccessMessageMixin,
                         UpdateView):
    pass


class MetadataListView(AdminRequiredMixin,
                       ListView):
    pass


class HomeView(AdminRequiredMixin, TemplateView):
    template_name = 'home.html'


class GeographicalScopesView(MetadataListView):
    model = models.GeographicalScope
    template_name = 'geographical_scopes.html'


class GeographicalScopesAddView(MetadataCreateView):
    model = models.GeographicalScope
    template_name = 'geographical_scopes_edit.html'
    success_message = 'Scope added successfully'

    def get_success_url(self):
        return reverse('geographical_scopes')


class GeographicalScopesEditView(MetadataUpdateView):
    model = models.GeographicalScope
    template_name = 'geographical_scopes_edit.html'
    success_message = 'Scope updated successfully'

    def get_success_url(self):
        return reverse('geographical_scopes')


class GeographicalScopesEnableDisableView(MetadataEnableDisableView):
    model = models.GeographicalScope
    success_message = 'Scope updated successfully'

    def get_success_url(self):
        return reverse('geographical_scopes')


class EnvironmentalThemesView(MetadataListView):
    model = models.EnvironmentalTheme
    template_name = 'environmental_themes.html'


class EnvironmentalThemesAddView(MetadataCreateView):
    model = models.EnvironmentalTheme
    template_name = 'environmental_themes_edit.html'
    success_message = 'Theme added successfully'

    def get_success_url(self):
        return reverse('environmental_themes')


class EnvironmentalThemeEditView(MetadataUpdateView):
    model = models.EnvironmentalTheme
    template_name = 'environmental_themes_edit.html'
    success_message = 'Theme updated successfully'

    def get_success_url(self):
        return reverse('environmental_themes')


class EnvironmentalThemeEnableDisableView(MetadataEnableDisableView):
    model = models.EnvironmentalTheme
    success_message = 'Theme updated successfully'

    def get_success_url(self):
        return reverse('environmental_themes')


class CountriesView(MetadataListView):
    model = models.Country
    template_name = 'countries.html'


class CountriesAddView(MetadataCreateView):
    model = models.Country
    template_name = 'countries_edit.html'
    success_message = 'Country added successfully'

    def get_success_url(self):
        return reverse('countries')


class CountryEditView(MetadataUpdateView):
    model = models.Country
    template_name = 'countries_edit.html'
    success_message = 'Country updated successfully'
    form_class = CountryEditForm

    def get_success_url(self):
        return reverse('countries')


class CountryEnableDisableView(MetadataEnableDisableView):
    model = models.Country
    success_message = 'Country updated successfully'

    def get_success_url(self):
        return reverse('countries')


class MetadataUpdateOrder(MetadataUpdateView):

    METADATA_NAME_TO_MODEL = {
        'geoscope': models.GeographicalScope,
        'envtheme': models.EnvironmentalTheme,
        'country': models.Country,
    }

    def post(self, request, *args, **kwargs):
        model_name = kwargs.get('metadata_name', None)
        items = self.request.POST.getlist('items[]')

        if not model_name in self.METADATA_NAME_TO_MODEL:
            return Http404

        for sort_idx, pk in enumerate(items):
            entry = get_object_or_404(
                self.METADATA_NAME_TO_MODEL[model_name], pk=pk)
            entry.sort_id = sort_idx
            entry.save()

        return HttpResponse()
