from django import forms
from django.core.urlresolvers import reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic import UpdateView

from flis_metadata.common import models


class EnableDisableForm(forms.ModelForm):
    class Meta:
        model = models.ReplicatedModel
        fields = ['is_deleted']


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
