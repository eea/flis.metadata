"""Dynamically add resources for ReplicatedModel classes in models.py."""
from flis_metadata.common.models import get_replicated_models

from tastypie.resources import ModelResource


def build_resource(model_name, cls):
    """Build a resource from a base class."""
    name = model_name + "Resource"

    # Build meta class
    Meta = type('Meta', (object, ), {
        'allowed_methods': ['get'],
        'queryset': cls.objects.all(), })

    Resource = type(name, (ModelResource, ), {'Meta': Meta})

    return Resource


# Append any other custom resources to this list
resources = [build_resource(name, cls) for name, cls in get_replicated_models()]
