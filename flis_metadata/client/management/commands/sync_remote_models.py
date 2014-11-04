import requests
import json

from django.conf import settings
from django.core.management.base import BaseCommand
from flis_metadata.common.models import *

from requests.exceptions import ConnectionError


class RemoteException(Exception):
    pass


MAX_REQUESTS = 100


def get_model_instances(model):
    """For a given model get all instances using the remote API."""
    name = model.__name__
    endpoint = (settings.METADATA_REMOTE_HOST +
                '/api/v1/{0}/?format=json'.format(name.lower()))

    objects = []
    for _ in xrange(MAX_REQUESTS):
        try:
            response = requests.get(endpoint)
        except ConnectionError:
            raise RemoteException(
                'Error reaching remote endpoint: {0}'.format(endpoint))

        if response.status_code != 200:
            raise RemoteException(
                'Bad response for endpoint: {0}'.format(endpoint))

        response_obj = json.loads(response.text)

        objects += response_obj['objects']
        if not response_obj['meta']['next']:
            break

        endpoint = settings.METADATA_REMOTE_HOST + response_obj['meta']['next']

    return objects


class Command(BaseCommand):
    help = 'Sync remote models on local database'

    def handle(self, *args, **options):
        r = get_model_instances(GeographicalScope)
        print len(r)
