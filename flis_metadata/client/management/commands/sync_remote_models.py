from django.core.management.base import BaseCommand
from flis_metadata.common.models import *


class Command(BaseCommand):
    help = 'Sync remote models on local database'

    def handle(self, *args, **options):
        print 'Not implemented yet!'
