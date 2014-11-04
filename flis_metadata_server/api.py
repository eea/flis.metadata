"""Dynamically add resources for ReplicatedModel classes in models.py."""
import inspect
import sys

from flis_metadata_server.models import ReplicatedModel

from tastypie.resources import ModelResource


def is_replicated_model(cls):
    """Check wether a class is a model to be replicated.

    This is implementend by extracting all models that inherit from
    ReplicatedModel
    """
    return (inspect.isclass(cls) and
            issubclass(cls, ReplicatedModel) and
            cls != ReplicatedModel)


def build_resource(model_name, cls):
    """Build a resource from a base class."""
    name = model_name + "Resource"

    # Build meta class
    Meta = type('Meta', (object, ), {
        'allowed_methods': ['get'],
        'queryset': cls.objects.all(), })

    Resource = type(name, (ModelResource, ), {'Meta': Meta})

    return Resource


replicated_models = inspect.getmembers(
    sys.modules['flis_metadata_server.models'], is_replicated_model)


# Append any other custom resources to this list
resources = [build_resource(name, cls) for name, cls in replicated_models]
