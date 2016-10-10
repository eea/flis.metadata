from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from tastypie.api import Api

from flis_metadata.server import views
from flis_metadata.server.api import resources

v1_api = Api(api_name="v1")
for resource in resources:
    v1_api.register(resource())


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(v1_api.urls)),

    url(r'^$', views.HomeView.as_view(), name='home_view'),

    url(r'^geographical_scopes/$', views.GeographicalScopesView.as_view(),
        name='geographical_scopes'),
    url(r'^geographical_scopes/new$',
        views.GeographicalScopesAddView.as_view(),
        name='geographical_scopes_edit'),
    url(r'^geographical_scopes/(?P<pk>\d+)/edit$',
        views.GeographicalScopesEditView.as_view(),
        name='geographical_scopes_edit'),
    url(r'^geographical_scopes/(?P<pk>\d+)/enable_disable$',
        views.GeographicalScopesEnableDisableView.as_view(),
        name='geographical_scopes_enable_disable'),

    url(r'^countries/$', views.CountriesView.as_view(),
        name='countries'),
    url(r'^countries/new$',
        views.CountriesAddView.as_view(),
        name='countries_edit'),
    url(r'^environmental_themes/(?P<pk>\w{2})/edit$',
        views.CountryEditView.as_view(),
        name='countries_edit'),
    url(r'^environmental_themes/(?P<pk>\w{2})/enable_disable$',
        views.CountryEnableDisableView.as_view(),
        name='countries_enable_disable'),

    url(r'^environmental_themes/$', views.EnvironmentalThemesView.as_view(),
        name='environmental_themes'),
    url(r'^environmental_themes/new$',
        views.EnvironmentalThemesAddView.as_view(),
        name='environmental_themes_edit'),
    url(r'^environmental_themes/(?P<pk>\d+)/edit$',
        views.EnvironmentalThemeEditView.as_view(),
        name='environmental_themes_edit'),
    url(r'^environmental_themes/(?P<pk>\d+)/enable_disable$',
        views.EnvironmentalThemeEnableDisableView.as_view(),
        name='environmental_themes_enable_disable'),
    url(r'^(?P<metadata_name>[^/]+)/update_order$',
        views.MetadataUpdateOrder.as_view(),
        name='update_order'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
