# -*- mode: python; coding: utf-8 -*-
"""Register our models for the admin UI
"""

# INPROD: I would find ways of divorcing the "admin" stuff from the production
# instance.

from django.contrib import admin
from .models import Person, Degree

admin.site.register(Person)
admin.site.register(Degree)
