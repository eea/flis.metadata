import json

from django.conf import settings
from django.test import TestCase
from mock import patch
from requests.exceptions import ConnectionError

from flis_metadata.common.models import GeographicalScope
from flis_metadata.common.tests.factories import GeographicalScopeFactory

from flis_metadata.client.management.commands import sync_remote_models


RESPONSE_FIXTURE = {
    'meta': {'limit': 20,
             'next': None,
             'offset': 0, 'previous': None,
             'total_count': 0},
    'objects': []
}

API_PREFIX = '/api/v1/geographicalscope/'


def get_geo_scope_fixture(objects, api_prefix=API_PREFIX,
                          next_page=None, prev_page=None):
    response = RESPONSE_FIXTURE.copy()
    response_obj = []

    for obj_id, obj in enumerate(objects):
        response_obj.append({'id': obj_id + 1,
                             'require_country': obj.require_country,
                             'title': obj.title,
                             'resource_uri': '{0}{1}/'.format(api_prefix,
                                                              obj_id + 1)})

    response['meta']['total_count'] = len(objects)
    response['meta']['next'] = next_page
    response['meta']['previous'] = prev_page
    response['objects'] = response_obj
    return json.dumps(response)


class GetMock(object):
    """Simulates a GET on the API endpoint for a list of given objects."""
    def __init__(self, objects, res_per_page=20):
        # Paginate input object list
        obj_pages = [objects[i:i + res_per_page]
                     for i in range(0, len(objects), res_per_page)]

        # Urls for other pages will simply be
        # /2 /3 /4 ...
        page_urls = ['/{0}'.format(i + 2) for i in range(len(obj_pages) - 1)]
        next_pages = page_urls + [None]

        # Assume that for every other url first page will be presented
        self.default = get_geo_scope_fixture(obj_pages[0],
                                             next_page=next_pages[0])

        self.responses = {}
        # Other calls should just follow the next field in meta
        for i, url in enumerate(page_urls):
            fixture = get_geo_scope_fixture(obj_pages[i + 1],
                                            next_page=next_pages[i + 1])
            self.responses[settings.METADATA_REMOTE_HOST + url] = fixture

    def __call__(self, url):
        return ResponseMock(self.responses.get(url, self.default))


class ResponseMock(object):
    def __init__(self, text, status_code=200):
        self.text = text
        self.status_code = status_code


class SyncRemoteModelsTest(TestCase):
    def setUp(self):
        self.instance_no = 10
        self.objects = [GeographicalScopeFactory()
                        for _ in range(self.instance_no)]

    @patch('flis_metadata.client.management.commands.'
           'sync_remote_models.requests.get')
    def test_geographical_scope_is_updated(self, get_mock):
        new_objects = self.objects[:]
        changed_pk = 5
        new_objects[changed_pk - 1].title = 'something new'

        get_mock.return_value = ResponseMock(get_geo_scope_fixture(new_objects))

        sync_remote_models.update_model_instances('GeographicalScope',
                                                  GeographicalScope)
        self.assertEqual(GeographicalScope.objects.get(pk=changed_pk).title,
                         'something new')

    @patch('flis_metadata.client.management.commands.'
           'sync_remote_models.requests.get')
    def test_new_geographical_scope_is_added(self, get_mock):
        new_objects = self.objects[:]
        new_objects.append(GeographicalScope(title='something new'))

        get_mock.return_value = ResponseMock(get_geo_scope_fixture(new_objects))
        sync_remote_models.update_model_instances('GeographicalScope',
                                                  GeographicalScope)

        new_title = GeographicalScope.objects.get(pk=self.instance_no + 1).title
        self.assertEqual(new_title, 'something new')

    @patch('flis_metadata.client.management.commands.'
           'sync_remote_models.requests.get')
    def test_exception_raised_on_bad_request(self, get_mock):
        get_mock.side_effect = ConnectionError()
        self.assertRaises(sync_remote_models.RemoteException,
                          sync_remote_models.get_model_instances,
                          'GeographicalScope',
                          GeographicalScope)

    @patch('flis_metadata.client.management.commands.'
           'sync_remote_models.requests.get')
    def test_exception_raised_on_404(self, get_mock):
        get_mock.return_value = ResponseMock('', 404)
        self.assertRaises(sync_remote_models.RemoteException,
                          sync_remote_models.get_model_instances,
                          'GeographicalScope',
                          GeographicalScope)

    def test_pagination(self):
        self.objects += [GeographicalScopeFactory() for _ in range(100)]
        expected_titles = [
            gs.title for gs in GeographicalScope.objects.all().order_by('pk')
        ]

        with patch('flis_metadata.client.management.commands.'
                   'sync_remote_models.requests.get', GetMock(self.objects)):
            objs = sync_remote_models.get_model_instances('GeographicalScope',
                                                          GeographicalScope)
            returned_titles = [o['title'] for o in objs]

            self.assertEqual(expected_titles, returned_titles)
