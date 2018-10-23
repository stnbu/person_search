# -*- mode: python; coding: utf-8 -*-
"""Generally speaking, we should use the most minimal Django installation
possible. These settings should be scrutinized and pared down in production.
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
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
]

MIDDLEWARE = [
    # INPROD: we should include only the essential here.
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
                'django.contrib.auth.context_processors.auth',
            ],
        },
    },
]

# INPROD: Not used by us but would be used in production, unless there's a
# better solution. This POC uses the built in Django DEVELOPMENT web server.
#WSGI_APPLICATION = 'person_search.wsgi.application'

SQLITE_DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        # INPROD: sqlite is only for testing. This absolute path makes things
        # easier.
        'NAME': os.path.join('/tmp/person_search.sqlite3'),
    }
}

POSTGRES_DATABASES = {
    'default': {
        'NAME': 'person_search',
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': 'localhost',
        'USER': 'person_search',
        'PASSWORD': 'password'
    },
}

# INPROD: This is hacky, but the point is to allow database "profile" selection
# at the command line. In production sqlite wouldn't be here at all.
_DB_CHOICE = os.getenv('PERSON_SEARCH_RDBMS', '').upper()
if _DB_CHOICE == 'POSTGRES':
    DATABASES = POSTGRES_DATABASES
elif _DB_CHOICE == 'SQLITE':
    DATABASES = SQLITE_DATABASES
else:
    DATABASES = SQLITE_DATABASES
    # or we could require it be explicit...
    # raise RuntimeError('Please set PERSON_SEARCH_RDBMS to one of [POSTGRES, '
    #                   'SQLITE]')

# INPROD: we should care about this stuff
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
# INPROD: let our fast, secure web server/cdn serve static directly.
STATIC_URL = '/static/'
