from factory import DjangoModelFactory
from factory import fuzzy

from flis_metadata.common import models


class GeographicalScopeFactory(DjangoModelFactory):
    class Meta:
        model = models.GeographicalScope

    title = fuzzy.FuzzyText()
    require_country = False
