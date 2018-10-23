# -*- mode: python; coding: utf-8 -*-
"""``person_search``. Crawl web pages for profiles, record results in an encrypted database and generate a pie chart displaying "percent persons with masters".
"""

# INPROD: We would have a smarter logging system. I just set everthing to debug here.
import logging
logging.basicConfig(level=logging.DEBUG)
