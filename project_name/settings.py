# https://docs.djangoproject.com/en/1.7/topics/settings/
# https://docs.djangoproject.com/en/1.7/ref/settings/
import os
import six
from getenv import env


PROJECT_SLUG = env('PROJECT_SLUG', '{{ project_name }}')


DEBUG = env('DEBUG', True)
TEMPLATE_DEBUG = DEBUG

# Server configuration
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ROOT_URLCONF = '%s.urls' % PROJECT_SLUG
WSGI_APPLICATION = '%s.wsgi.application' % PROJECT_SLUG

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
# STATICFILES_DIRS = (
#     os.path.join(PROJECT_PATH, 'static'),
#     os.path.join(BASE_DIR, 'static'),
#     '/app/staticfiles',
# )
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
# STATICFILES_STORAGE = 'require_s3.storage.OptimizedCachedStaticFilesStorage'

AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY', '')
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME', '')
AWS_AUTO_CREATE_BUCKET = True
AWS_HEADERS = { 'Cache-Control': 'public, max-age=86400', }
AWS_QUERYSTRING_AUTH = False
S3_BUCKET = env('S3_BUCKET', PROJECT_SLUG)
AWS_S3_FILE_OVERWRITE = False
AWS_S3_SECURE_URLS = True
AWS_REDUCED_REDUNDANCY = False
AWS_IS_GZIPPED = False


if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_HOST = 'smtp.sendgrid.net'
    EMAIL_HOST_USER = env('SENDGRID_USERNAME', '')
    EMAIL_HOST_PASSWORD = env('SENDGRID_PASSWORD', '')
    EMAIL_PORT = 25
    EMAIL_USE_TLS = False



# Conventions: https://docs.djangoproject.com/en/1.6/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_TZ = True
USE_I18N = True
USE_L10N = True

# Security
if not DEBUG:
    ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '%s-server.herokuapp.com' % PROJECT_SLUG]
SECRET_KEY = env('SECRET_KEY', 'devsecretkey')


INSTALLED_APPS = (
    'django_admin_bootstrapped.bootstrap3',
    'django_admin_bootstrapped',

    'django.contrib.admin',
    # 'django.contrib.admin.apps.SimpleAdminConfig'
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'django_extensions',
    'toolbox',

    'django_cas',

    'polymorphic',
    'tastypie',

    # App
    'accounts_bootstrap3',
    '%s_api' % PROJECT_SLUG,
    '%s_site' % PROJECT_SLUG,

    # Test
    # 'adminplus',
    # 'django_filters',

    'paypal.standard',
    'paypal.pro',

    'pinax_theme_bootstrap',
    'bootstrapform',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
)

if DEBUG:
    INSTALLED_APPS += (
        'debug_toolbar.apps.DebugToolbarConfig',
        'django_nose',
        'django_coverage',
    )

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader'
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'allauth.account.context_processors.account',
    'allauth.socialaccount.context_processors.socialaccount',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'django_cas.backends.CASBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_cas.middleware.CASMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    if six.PY3:
        from urllib.parse import urlparse
    else:
        from urlparse import urlparse
    url = urlparse(env('DATABASE_URL', 'postgres://dev:dev@localhost:5432/%s' % PROJECT_SLUG))
    database = url.path[1:]
    user = url.username
    password = url.password
    host = url.hostname
    port = url.port

    # from psycopg2cffi import compat # PyPY Postgres driver
    # compat.register()
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            # 'ENGINE': 'django.db.backends.mysql',
            'NAME': database,
            'USER': user,
            'PASSWORD': password,
            'HOST': host,
            'PORT': port,
        }
    }


# django-cas
CAS_SERVER_URL = 'http://127.0.0.1:8000'
CAS_SERVER_SSL_VERIFY = True
CAS_SERVER_SSL_CERT = None
CAS_LOGOUT_COMPLETELY = True
CAS_SINGLE_SIGN_OUT = True
CAS_RENEW = False
CAS_GATEWAY = False
CAS_REDIRECT_URL = '/'
CAS_IGNORE_REFERER = False
CAS_RETRY_LOGIN = False
CAS_AUTO_CREATE_USERS = False

AUTH_PROFILE_MODULE = '%s_api.Account' % PROJECT_SLUG

SITE_ID = env('SITE_ID', 1)
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_SUBJECT_PREFIX = '[%s] ' % PROJECT_SLUG
# ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'
ACCOUNT_PASSWORD_MIN_LENGTH = 8
LOGIN_REDIRECT_URL = '/'

# django-merchant
MERCHANT_TEST_MODE = DEBUG
MERCHANT_SETTINGS = {
    'pay_pal': {
        'WPP_USER': env('PAYPAL_WPP_USER', '?'),
        'WPP_PASSWORD': env('PAYPAL_WPP_PASSWORD', '?'),
        'WPP_SIGNATURE': env('PAYPAL_WPP_SIGNATURE', '?'),
    }
}

# django-paypal
PAYPAL_TEST = MERCHANT_TEST_MODE
PAYPAL_WPP_USER = MERCHANT_SETTINGS['pay_pal']['WPP_USER']
PAYPAL_WPP_PASSWORD = MERCHANT_SETTINGS['pay_pal']['WPP_PASSWORD']
PAYPAL_WPP_SIGNATURE = MERCHANT_SETTINGS['pay_pal']['WPP_SIGNATURE']
PAYPAL_RECEIVER_EMAIL = 'paulocheque@gmail.com'

# django-tastypie
API_LIMIT_PER_PAGE = 50
TASTYPIE_FULL_DEBUG = DEBUG
TASTYPIE_ALLOW_MISSING_SLASH = True
TASTYPIE_DATETIME_FORMATTING = 'iso-8601-strict'
TASTYPIE_DEFAULT_FORMATS = ['json', 'xml']
