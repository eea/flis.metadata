from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from tastypie.api import Api

from flis_metadata.server import views
from flis_metadata.server.api import resources

v1_api = Api(api_name="v1")
for resource in resources:
    v1_api.register(resource())


urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(v1_api.urls)),

    url(r'^$', views.HomeView.as_view(), name='home_view'),
    url(r'^geographical_scopes/$', views.GeographicalScopesView.as_view(),
        name='geographical_scopes'),
    url(r'^countries/$', views.GeographicalScopesView.as_view(),
        name='countries'),
    url(r'environmental_themes/$', views.GeographicalScopesView.as_view(),
        name='environmental_themes'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
