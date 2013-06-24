# Django settings for src project.
import os
import sys
import logging

# is ./manage.py test invoked ?
TEST = 'test' in sys.argv

# is ./manage.py runserver invoked ?
DEBUG = 'runserver' in sys.argv

TEMPLATE_DEBUG = DEBUG
DEFAULT_CHARSET = 'utf-8'
BASE = os.path.dirname(os.path.abspath(__file__))


ADMINS = (
    ('Openpaste.org Administrator', 'gorej@codescale.net'),
)

GENERAL_SUPPORT_EMAIL = ADMINS[0][1]

MANAGERS = ADMINS

if TEST:
    # tests db
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'openpaste',
            'USER': 'openpaste',
            'PASSWORD': '',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Bratislava'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(BASE, 'site-media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/site-media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin-media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'vcj_g3lm)&#hzgku)u7ehs8rv4p7%_bu*wv2%3jl9hv(&^lzuv'

# Antispam secret key
ANTISPAM_KEY = '3453151o43oofu87^&*^S^DhsU'

VISITOR_COOKIE_NAME = 'visitor_uuid'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE, 'templates')
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'web.context_processors.common_data'
)

MIDDLEWARE_CLASSES = (
    'web.middleware.VisitorMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.transaction.TransactionMiddleware'
)

ROOT_URLCONF = 'src.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE, 'templates')
)

INSTALLED_APPS = (
    #'django.contrib.auth',
    #'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    #'django.contrib.admin',
    'web',
    'gunicorn',
)

VIEWABLE_SYNTAXES = tuple(
    #'HTML', 'XML', 'XSLT'
)

LOG_BASE_PATH =  BASE + os.sep + 'logs'

class LevelFilter(logging.Filter):
    def __init__(self, name='', level=None):
        self.level = level

    def filter(self, record):
        if self.level is None:
            return True
        return self.level == record.levelname

# ENABLE_FULL_LOG_IN_PRODUCTION is set to True, file_all handler is appended even if settings.DEBUG=False (production run)
ENABLE_FULL_LOG_IN_PRODUCTION = True

LOGGER_PERFORMANCE = 'performance'

LOGGING_LEVEL_FILTER = LevelFilter

LOGGING = {
    'version' : 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(asctime)s %(levelname)s %(message)s'
        },
    },
    'filters': {
        'debug_filter': {
            '': 'LevelFilter',
            'level': 'DEBUG'
        },
        'info_filter': {
            '': 'LevelFilter',
            'level': 'INFO'
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler'
        },
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'console_warnings':{
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file_all': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'simple',
            'filename': os.path.join(LOG_BASE_PATH, 'all.log'),
            'mode': 'a'
        },
        'file_performance': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'simple',
            'filename': os.path.join(LOG_BASE_PATH, 'performance.log'),
            'mode': 'a'
        },
        'file_sql': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'simple',
            'filename': os.path.join(LOG_BASE_PATH, 'sql.log'),
            'mode': 'a'
        },
        'file_info': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'simple',
            'filename': os.path.join(LOG_BASE_PATH, 'info.log'),
            'mode': 'a',
            'filters': ['info_filter']
        },
        'file_debug': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'simple',
            'filename': os.path.join(LOG_BASE_PATH, 'debug.log'),
            'mode': 'a',
            'filters': ['debug_filter']
        },
        'file_error': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'formatter': 'simple',
            'filename': os.path.join(LOG_BASE_PATH, 'error.log'),
            'mode': 'a'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        '': {
            'handlers': ['file_info', 'file_error'],
            'level': 'DEBUG'
        },
        'django.db.backends': {
            'propagate': False,
            'handlers': ['file_sql'],
            'level': 'DEBUG'
        },
        LOGGER_PERFORMANCE: {
            'propagate': False,
            'handlers': ['file_performance'],
            'level': 'DEBUG'
        },
    }
}

if DEBUG:
    LOGGING['loggers']['']['handlers'] += ['file_all', 'file_debug', 'console_warnings']
    LOGGING['loggers']['django.db.backends']['handlers'] += ['file_all']
    LOGGING['loggers'][LOGGER_PERFORMANCE]['handlers'] += ['console', 'file_all']
else:
    if ENABLE_FULL_LOG_IN_PRODUCTION:
        LOGGING['loggers']['']['handlers'] += ['file_all']
        LOGGING['loggers']['django.db.backends']['handlers'] += ['file_all']
        LOGGING['loggers'][LOGGER_PERFORMANCE]['handlers'] += ['file_all']
    LOGGING['loggers']['']['handlers'] += ['mail_admins']
