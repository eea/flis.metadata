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
