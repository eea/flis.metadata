import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

# disable frame.Loader in tests, don't need it
TEMPLATE_LOADERS = ('django.template.loaders.app_directories.Loader',)

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

USER_ID = 'tester'
USER_GROUPS = []
USER_ROLES = ['Administrator']

VIEW_ROLES = ('Administrator', 'Contributor', 'Viewer')
EDIT_ROLES = ('Administrator', 'Contributor')


