import inspect
import sys

from django.db.models import BooleanField
from django.db.models import CharField
from django.db.models import Model


class ReplicatedModel(Model):

    class Meta:
        abstract = True


class GeographicalScope(ReplicatedModel):

    title = CharField(max_length=128)
    require_country = BooleanField(default=False)

    class Meta:
        ordering = ('-pk',)

    def __unicode__(self):
        return self.title


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
