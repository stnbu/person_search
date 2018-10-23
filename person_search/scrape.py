# -*- mode: python; coding: utf-8 -*-
"""Crawl and Scrape!

This is a very simple, straightforward web crawler that makes a few assumptions
for simplicity's sake (see ``README.md``). You may run it from the command line,
but it requires that *our* web server is running and listening on port 8000. So
before running, please run:

    python manage.py runserver

...in a separate terminal.

This crawler re-uses the Django ORM. Note that (as with all django usage) it is
necessary to set ``DJANGO_SETTINGS_MODULE`` before executing. For example, to
run this module as a script:

    DJANGO_SETTINGS_MODULE=person_search.settings python scrape.py

A ``db`` object is imported. This module contains the table classes from
``models``. This is a ``global()`` symbol, but I pass it to the crawl function
as an argument, which (to me) makes the code read better.
"""

import os
from person_search import db
from bs4 import BeautifulSoup
import requests

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def scrape_person(content):
    """Scrape well-formatted html, extracting person information
    """
    soup = BeautifulSoup(content)
    person = {}
    for parameter in [
            'full_name',
            'email',
            'gender',
            'degree_name',
            'institution',
    ]:
        person[parameter] = soup.find(
            'div', {'id': parameter}).get_text().strip()
    return person


def crawl(emails, db):
    """Given an iterable of email address (strings), fetch the profile web page,
    scrape, and insert into database.
    """
    for email in emails:

        email = email.strip()  # emails are stored/compared as lower-case, so
        # strip() is enough

        if db.Person.objects.filter(email=email):
            logger.info('we already have a record for email: %s' % email)
            continue

        url = 'http://127.0.0.1:8000/person_profile/%s/' % email
        response = requests.get(url)
        if response.status_code != 200:
            logger.warn('scraping "%s" resulted in status %s' %
                        (email, response.status_code))
            continue

        raw_scrape_data = scrape_person(response.content)
        degree_data = {
            'name': raw_scrape_data['degree_name'],
            'institution': raw_scrape_data['institution'],
        }
        if not degree_data['name'] and not degree_data['institution']:
            degree = None
        else:
            # I believe this is faster than a try/except that catches
            # ``IntegrityError``. If catching ``IntegrityError`` we'd have to
            # create a transaction and roll back. Worth investigating more,
            # though.
            existing = db.Degree.objects.filter(**degree_data)
            if not existing:
                degree = db.Degree(**degree_data)
                degree.save()
            else:
                degree, = existing

        # We assume data doesn't change (see ``README.md``) and we check for the
        # email at the top of this loop, so we should be able to add here
        # without integrity problems.
        person_data = {
            'full_name': raw_scrape_data['full_name'],
            'email': raw_scrape_data['email'],
            'gender': raw_scrape_data['gender'],
            'degree': degree,
        }
        person = db.Person(**person_data)
        # INPROD: Saving with every pass of this loop is inefficient. Minimally
        # we should do something like batch them with
        #
        # >>> insertions = []
        # >>> for person_data in data:
        # >>>     insertions.append(db.Person(**person_data))
        # >>> db.Person.objects.bulk_create(insertions)
        #
        # Maybe saving every n records...
        person.save()


if __name__ == '__main__':

    # Run a simple test scraping run using bundled email address lists as
    # input

    # Note that it's possible to get a pie chart for just the supplied data by
    # limiting the below loop to *only* ``actual_persons_email_addresses.txt``

    resources = os.path.join(os.path.dirname(__file__), 'resources')
    for address_file in ['actual_persons_email_addresses.txt',
                         'random_email_addresses.txt']:
        with open(os.path.join(resources, address_file)) as f:
            crawl(f, db)
