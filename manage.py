#!/usr/bin/env python
# -*- mode: python; coding: utf-8 -*-
"""Helper script to use ``manage.py``. It might make sense to extend ``manage``
so that it can run the scraper. e.g. ``python manage.py scrape``.
"""
import os
import sys
from django.core.management import execute_from_command_line

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'person_search.settings')
    execute_from_command_line(sys.argv)
