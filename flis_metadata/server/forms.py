from django import forms

from flis_metadata.common import models


class EnableDisableForm(forms.ModelForm):
    fields = ['is_deleted']

    class Meta:
        model = models.ReplicatedModel


class CountryEditForm(forms.ModelForm):
    fields = ['name']

    class Meta:
        model = models.Country
        exclude = ['iso']
