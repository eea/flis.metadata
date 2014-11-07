from django.conf.urls import patterns, include, url
from django.contrib import admin
from tastypie.api import Api

from flis_metadata.server.api import resources

v1_api = Api(api_name="v1")
for resource in resources:
    v1_api.register(resource())


urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(v1_api.urls)),
)
