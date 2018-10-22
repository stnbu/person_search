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

        print(parameter, '<'*20)
        person[parameter] = soup.find('div', {'id': parameter}).get_text().strip()
    return person

def crawl(emails):
    """Given an iterable of email address (strings), fetch the profile web page, scrape, and insert into database.
    """
    for email in emails:

        url = 'http://127.0.0.1:8000/test_person/%s' % email.lower().strip()
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
            degree = db.Degree(**degree_data)
            try:
                degree.save()
            except IntegrityError:
                logger.warn('Tried to add existing degree: %s' % repr(degree))
        person_data = {
            'full_name': raw_scrape_data['full_name'],
            'email': raw_scrape_data['email'],
            'gender': raw_scrape_data['gender'],
            'degree': degree,
        }
        person = db.Person(**person_data)
        person.save()

if __name__ == '__main__':
        with open('/home/mburr/git/person_search/person_search/resources/actual_persons_email_addresses.txt') as f:
            crawl(f)

# def readthing():
#     print(db.Person.objects.filter(full_name__icontains='%'))
#     print(db.Person.objects.filter(full_name='Bob Example'))
#     print(db.Person.objects.all())
# def writethings():
#     insertions = []
#     degrees = {}
#     for i in range(1, 5):
#         degrees[i] = db.Degree(name='foo', institution='bar%s' % i)
#         degrees[i].save()
#     for name, email, degree in [
#             ('Mary Blarge', 'mary@example.com', 1),
#             ('Zoo Keeper', 'zoo@example.com', 2),
#             ('Mr Joe', 'kenm@example.com', 3),
#             ('Bob Example', 'bob@example.com', 4),
#     ]:
#         insertions.append(db.Person(full_name=name, email=email, degree=degrees[degree]))
#     # NOTE: `.save()` done by django orm after `bulk_create`
#     db.Person.objects.bulk_create(insertions)
# def main():
#     script_basename, _ = os.path.splitext(os.path.basename(__file__))
