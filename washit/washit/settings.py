"""
Django settings for washit project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ch7tg#y0%5&-5n6f&yu#6run*9*hpkwmnq@+fp(0ns(&3-+&tc'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'anyclean',

    # The Django sites framework is required
    'django.contrib.sites',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    'widget_tweaks',
    'tokenapi',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)


ROOT_URLCONF = 'washit.urls'

WSGI_APPLICATION = 'washit.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'anyclean',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    }
}


TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',

    # `allauth` specific context processors
    'allauth.account.context_processors.account',
    'allauth.socialaccount.context_processors.socialaccount',
)


AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend"
)

ACCOUNT_AUTHENTICATION_METHOD = 'username_email'

ACCOUNT_FORMS = ({'signup': 'anyclean.forms.MySignupForm'})

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


LOGIN_URL = '/accounts/login/'
LOGOUT_URL = '/logout/'
LOGIN_REDIRECT_URL = '/dashboard_redirect/'

SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'SCOPE': ['email', 'public_profile'],
        'METHOD': 'js_sdk'  # instead of 'oauth2'
    }
}

# Token api
TOKEN_TIMEOUT_DAYS = 15
TOKEN_CHECK_ACTIVE_USER = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/var/www/anyclean/static/'

TEMPLATE_DIRS = (
    BASE_DIR + '/washit/templates/',
)

STATICFILES_DIRS = (
    BASE_DIR + '/washit/static/',
)


SITE_ID = 1

# Account Adapter Override
ACCOUNT_ADAPTER = "anyclean.adapter.DefaultAccountAdapter2"


# Email Configurations.
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = '587'
# # Credentials (if needed)
# EMAIL_HOST_USER = ‘$username’
# EMAIL_HOST_PASSWORD = ‘$password’

# DEFAULT_FROM_EMAIL = ‘$email’

# Print email on console.
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}