from factory import DjangoModelFactory
from factory import fuzzy


class GeographicalScopeFactory(DjangoModelFactory):
    FACTORY_FOR = 'common.GeographicalScope'

    title = fuzzy.FuzzyText()
    require_country = False
