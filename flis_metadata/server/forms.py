from django import forms

from flis_metadata.common import models


class EnableDisableForm(forms.ModelForm):

    class Meta:
        model = models.ReplicatedModel
        fields = ['is_deleted']


class CountryEditForm(forms.ModelForm):

    class Meta:
        model = models.Country
        fields = ['name']
