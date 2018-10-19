# -*- mode: python; coding: utf-8 -*-
"""
Generally speaking, we should use the most minimal Django installation possible. These settings should be scrutinized and pared down in production.
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# SECURITY WARNING: keep the secret key used in production secret!
# INPROD: Do something smart in production here!
SECRET_KEY = 'TRAd4KRErBaIpYlRvTxPRp5weohAsaRHvmanlegDemeLLESmwk0QbN8LBq3n'

# SECURITY WARNING: don't run with debug turned on in production!
# INPROD: I concur.
DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'person_search',
    # INPROD: In production, disable debug and admin entirely
    # maybe this for starters:  https://github.com/stnbu/oleo/blob/master/oleo/settings.py#L124
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    # INPROD: we should include only the essential here:
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'person_search.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # INPROD: we should include only the essential here:
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# INPROD: Not used by us but would be used in production, unless there's a better solution. This POC uses the built in Django DEVELOPMENT web server.
#WSGI_APPLICATION = 'person_search.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# AUTH_PASSWORD_VALIDATORS = [
#     {
#         'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
#     },
# ]

# INPROD: we should care about this stuff
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
# INPROD: let our fast, secure web server/cdn serve static directly.
STATIC_URL = '/static/'
