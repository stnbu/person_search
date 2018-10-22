# -*- mode: python; coding: utf-8 -*-
"""Crawl and Scrape!
"""

from person_search import db
from bs4 import BeautifulSoup
import requests
from django.db import IntegrityError

import logging
logging.basicConfig(level=logging.DEBUG)
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
        person[parameter] = soup.find('div', {'id': parameter}).get_text().strip()
    return person

def crawl(emails):
    """Given an iterable of email address (strings), fetch the profile web page, scrape, and insert into database.
    """
    for email in emails:

        email = email.strip()  # emails are stored/compared as lower-case, so strip() is enough

        if db.Person.objects.filter(email=email):
            logger.info('we alread have a record for email: %s' % email)
            continue

        url = 'http://127.0.0.1:8000/person_profile/%s' % email
        response = requests.get(url)
        if response.status_code != 200:
            logger.warn('scraping "%s" resulted in status %s' % (email, response.status_code))
            continue

        raw_scrape_data = scrape_person(response.content)
        degree_data = {
            'name': raw_scrape_data['degree_name'],
            'institution': raw_scrape_data['institution'],
        }
        if not degree_data['name'] and not degree_data['institution']:
            degree = None
        else:
            existing = db.Degree.objects.filter(**degree_data)
            if not existing:
                degree = db.Degree(**degree_data)
                degree.save()
            else:
                degree, = existing

        # We assume data doesn't change (see ``README.md``) and we check for the email at the top of this loop, so we should be able to add here without integrity problems.
        person_data = {
            'full_name': raw_scrape_data['full_name'],
            'email': raw_scrape_data['email'],
            'gender': raw_scrape_data['gender'],
            'degree': degree,
        }
        person = db.Person(**person_data)
        # INPROD: Saving with every pass of this loop is inefficient. Minimally we should do something like batch them with
        #
        # >>> insertions = []
        # >>> for person_data in data:
        # >>>     insertions.append(db.Person(**person_data))
        # >>> db.Person.objects.bulk_create(insertions)
        #
        # Maybe saving every n records...
        person.save()

if __name__ == '__main__':
        with open('/home/mburr/git/person_search/person_search/resources/actual_persons_email_addresses.txt') as f:
            crawl(f)
        with open('/home/mburr/git/person_search/person_search/resources/random_email_addresses.txt') as f:
            crawl(f)
