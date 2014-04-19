import os 
from rockgympro.settings import *
 
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ['RDS_DB_NAME'],
        'USER': os.environ['RDS_USERNAME'],
        'PASSWORD': os.environ['RDS_PASSWORD'],
        'HOST': os.environ['RDS_HOSTNAME'],
        'PORT': os.environ['RDS_PORT'],
    },
}

'''CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': os.environ['CACHE_URL'],
    }
}'''

DEFAULT_FROM_EMAIL = "noreply@dynoroute.com"

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    #'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]

INSTALLED_APPS += ('storages',)

#SESSION_ENGINE = "django.contrib.sessions.backends.cache"

DEFAULT_FILE_STORAGE = 'storages.backends.s3botomulti.S3BotoStorage_media'
STATICFILES_STORAGE = 'storages.backends.s3botomulti.S3BotoStorage_static'
EMAIL_BACKEND = 'django_ses.SESBackend'
THUMBNAIL_DEFAULT_STORAGE = 'storages.backends.s3botomulti.S3BotoStorage_media'

AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_KEY']

STORAGES_S3BOTO_MULTI = {
    'media' : {
        'AWS_ACCESS_KEY_ID' : os.environ['AWS_ACCESS_KEY_ID'],
        'AWS_SECRET_ACCESS_KEY' : os.environ['AWS_SECRET_KEY'],
        'AWS_STORAGE_BUCKET_NAME' : 'media.dynoroute.com',
        #'AWS_S3_SECURE_URLS' : False,
        #'AWS_S3_CUSTOM_DOMAIN' : "media.dynoroute.com",
        'AWS_QUERYSTRING_AUTH' : False
    },
    'static' : {
        'AWS_ACCESS_KEY_ID' : os.environ['AWS_ACCESS_KEY_ID'],
        'AWS_SECRET_ACCESS_KEY' : os.environ['AWS_SECRET_KEY'],
        'AWS_STORAGE_BUCKET_NAME' : 'static.dynoroute.com',
        #'AWS_S3_SECURE_URLS' : False,
        #'AWS_S3_CUSTOM_DOMAIN' : "static.dynoroute.com",
        'AWS_QUERYSTRING_AUTH' : False,
    }
}

STATIC_URL = "http://static.dynoroute.com/"

AWS_SES_REGION_NAME = 'us-east-1'
AWS_SES_REGION_ENDPOINT = 'email.us-east-1.amazonaws.com'

DEBUG = (os.environ.get("DEBUG", "FALSE") == "TRUE")
TEMPLATE_DEBUG = DEBUG
THUMBNAIL_DEBUG = DEBUG

for host in os.environ.get("ALLOWED_HOSTS", "").split():
    ALLOWED_HOSTS += [host]
