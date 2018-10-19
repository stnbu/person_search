# -*- mode: python; coding: utf-8 -*-
"""Use the Django ORM independently of the web UI. This involves some "tricks" but has the benefit of there being only one place to keep the database i/o logic. This is especially helpful if we're doing something to the data before storing (like encryption)
"""

# INPROD: I would very seriously reconsider this. It may be fine, but it may not be! It might be better to teach Django to use a different ORM, like sqlalchemy. Whatever the case, it's very helpful not to re-create database logic in two places. That's why this file...

import os
import importlib
import django

# I have removed some comments and strings to keep things anonymous. It's pretty easy to follow by just reading the code... (again, needs testing and rigor)

try:
    dsm_name = os.environ['DJANGO_SETTINGS_MODULE']
except KeyError:
    raise ImportError("set DJANGO_SETTINGS_MODULE")

globals().update(importlib.import_module(
    dsm_name).__dict__)

from django.conf import settings
from django.db import connections

try:
    settings.configure(DATABASES=DATABASES)
    django.setup()
except RuntimeError:
    pass

from person_search.models import *
