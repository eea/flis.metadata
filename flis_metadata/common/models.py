import inspect
import sys

from django.db.models import (
    BooleanField, CharField, Model, IntegerField,
)

class ReplicatedModel(Model):

    class Meta:
        abstract = True
        permissions = (
            ('config', 'Can change configuration'),
        )

    is_deleted = BooleanField(default=False)


class GeographicalScope(ReplicatedModel):

    title = CharField(max_length=128)
    require_country = BooleanField(default=False)
    sort_id = IntegerField(default=0, null=True, blank=True)

    class Meta:
        ordering = ('sort_id',)

    def __unicode__(self):
        return self.title


class EnvironmentalTheme(ReplicatedModel):

    title = CharField(max_length=128)
    sort_id = IntegerField(default=0, null=True, blank=True)

    class Meta:
        ordering = ('sort_id',)

    def __unicode__(self):
        return self.title


class Country(ReplicatedModel):

    iso = CharField(max_length=2, primary_key=True)
    name = CharField(max_length=128)
    sort_id = IntegerField(default=0, null=True, blank=True)

    class Meta:
        ordering = ('sort_id',)

    def __unicode__(self):
        return self.name


def _is_replicated_model(cls):
    """Check wether a class is a model to be replicated.

    This is implementend by extracting all models that inherit from
    ReplicatedModel
    """
    return (inspect.isclass(cls) and
            issubclass(cls, ReplicatedModel) and
            cls != ReplicatedModel)


def get_replicated_models():
    """Return all replicated models in this module."""
    return inspect.getmembers(sys.modules[__name__], _is_replicated_model)
