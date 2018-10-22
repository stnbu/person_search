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

SQLITE_DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        # INPROD: sqlite is only for testing. This absolute path makes things easier.
        'NAME': os.path.join('/tmp/person_search.sqlite3'),
    }
}

POSTGRES_DATABASES = {
    'default': {},
    'person_search_ro': {
        'NAME': 'person_search',
        'ENGINE': 'django.db.backends.postgresql',
        'USER': 'person_search_ro',
        'PASSWORD': 'password'
    },
    # INPROD: The read-write password is sitting right here next to the read-only one, so there's limited benefit to having different accounts with exactly this implmentation. In production, it's possible they would be running as separate users and possibly on separate hosts. In a single-master cluster for example.
    'person_search_rw': {
        'NAME': 'person_search',
        #'ENGINE': 'django.db.backends.postgresql',
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        #'HOST': '/run/postgresql',
        'HOST': 'localhost',
        'PORT': '',
        'USER': 'person_search_rw',
        'PASSWORD': 'password'
    },
}


####### FIXME FORNOW NOTE ########
####### FIXME FORNOW NOTE ########
POSTGRES_DATABASES['default'] = POSTGRES_DATABASES['person_search_rw']
####### FIXME FORNOW NOTE ########
####### FIXME FORNOW NOTE ########


# This is hacky, but the point is to allow database "profile" selection at the command line.
_DB_CHOICE = os.getenv('PERSON_SEARCH_RDBMS', '').upper()
if _DB_CHOICE == 'POSTGRES':
    DATABASES = POSTGRES_DATABASES
elif _DB_CHOICE == 'SQLITE':
    DATABASES = SQLITE_DATABASES
else:
    DATABASES = SQLITE_DATABASES
    #raise RuntimeError('Please set PERSON_SEARCH_RDBMS to one of [POSTGRES, '
    #                   'SQLITE]')


# INPROD: we should care about this stuff
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
# INPROD: let our fast, secure web server/cdn serve static directly.
STATIC_URL = '/static/'
