# Django settings for dataupload project.
import os

DEBUG = False
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

TEMPLATE_DEBUG = DEBUG

ROOT = os.path.dirname(os.path.abspath(__file__))
path = lambda *a: os.path.join(ROOT, *a)

ADMINS = (
    ('Josh Mize', 'jgmize@gmail.com'),
    ('Buddy Lindsey', 'percent20@gmail.com'),
    ('Jeremy Satterfield', 'jsatt22@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        # 'ENGINE': 'django.contrib.gis.db.backends.postgis', # For postgis instances
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'db.sqlite3',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'UTC'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = "%s/media" % path('.')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = "%s/static" % path('.')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
#ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
    'compressor.finders.CompressorFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '=1jbeb0%5xv^pskjxkuh#%vfna09z(5ng2#jy)h4y8iz(2l9^g'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    # 'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    "%s/templates" % path('.'),
)

INSTALLED_APPS = (
    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.gis',
    'django.contrib.humanize',
    'django.contrib.messages',
    'django.contrib.sessions',
    #'django.contrib.sites',
    'django.contrib.staticfiles',

    # Third-party
    'boundaryservice',
    'compressor',
    'django_extensions',
    'south',
    'tastypie',

    #WebDevs
    'boundary_demo',
    'datafile',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple':{'format': '%(levelname)s: %(message)s'}
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate':True
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'okdata': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate':True
        },
    }
}

COMPRESS_ENABLED = False

COMPRESS_ROOT = STATIC_ROOT

SHAPEFILES_SUBDIR = 'shapefiles'
SHAPEFILES_DIR = 'media/%s' % SHAPEFILES_SUBDIR

# Boundary Service demo settings
API_DOMAIN = 'www.oklahomadata.org/boundary'
EXAMPLE_SCOPE = 'Oklahoma'
EXAMPLE_BOUNDARY_SET = 'municipal boundary'
EXAMPLE_BOUNDARY_SETS = 'municipal boundaries' # plural
EXAMPLE_BOUNDARY_SET_CODE = 'municipal-boundaries'
EXAMPLE_BOUNDARY_SET_CODE_BIS = 'counties' # "bis" is latin for "again"
EXAMPLE_BOUNDARY_SET_RESPONSE = '''{
    "authority": "CSA",
    "boundaries": [
        "/boundary/1.0/boundary/achille-municipal-boundary/",
        "/boundary/1.0/boundary/adair-municipal-boundary/",
        ...
        ...
        ...
        "/boundary/1.0/boundary/yeager-municipal-boundary/",
        "/boundary/1.0/boundary/yukon-municipal-boundary/",
        "/boundary/1.0/boundary/yukon-municipal-boundary-2/"
    ],
    "count": 1485,
    "domain": "Oklahoma",
    "href": "",
    "last_updated": "2012-03-15",
    "metadata_fields": [
        "ST_FIPS",
        "CO_FIPS",
        "CITYNAME",
        "FIPS",
        "FIPSCC",
        "AD_VAL_NUM",
        "LAST_ANNEX",
        "LAST_VERIF",
        "REMARKS"
    ],
    "name": "Municipal Boundaries",
    "notes": "",
    "resource_uri": "/boundary/1.0/boundary-set/municipal-boundaries/",
    "slug": "municipal-boundaries"

}'''
EXAMPLE_BOUNDARY = 'Tulsa County'
EXAMPLE_BOUNDARY_CODE = 'tulsa-county'
EXAMPLE_BOUNDARY_RESPONSE = '''{
    "centroid": {
        "coordinates": [
            -95.941506,
            36.121079
        ],
        "type": "Point"
    },
    "external_id": "143",
    "kind": "County",
    "metadata": {
        "COUNTY": 143,
        "NAME": "TULSA",
        "STATE": 40,
        "STATEPLANE": "N"
    },
    "name": "TULSA",
    "resource_uri": "/boundary/1.0/boundary/tulsa-county/",
    "set": "/boundary/1.0/boundary-set/counties/",
    "simple_shape": {
        "coordinates": [
            [
                [
                    [
                        -95.761625,
                        35.973807
                    ],
                    [
                        -95.761563,
                        35.9065
                    ],
                    ...
                    ...
                    ...,
                    [
                        -95.761683,
                        36.162672
                    ],
                    [
                        -95.761763,
                        36.085538
                    ],
                    [
                        -95.761625,
                        35.973807
                    ]
                ]
            ]
        ],
        "type": "MultiPolygon"
    },
    "slug": "tulsa-county"

}'''
EXAMPLE_PLACE = 'Fab Lab Tulsa'
EXAMPLE_PLACE_LAT_LNG = '36.15061,-95.958351'
EXAMPLE_UNIT = 'mile'
EXAMPLE_UNIT_CODE = 'mi'
# End Boundary Service demo settings

try:
    from settings_local import *
except ImportError:
    pass
else:
    try:
        INSTALLED_APPS += LOCAL_INSTALLED_APPS
    except:
        pass
    try:
        MIDDLEWARE_CLASSES += LOCAL_MIDDLEWARE_CLASSES
    except:
        pass
