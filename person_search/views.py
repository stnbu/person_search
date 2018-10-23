# -*- mode: python; coding: utf-8 -*-
"""Straightforward, function-based views. Since we read and write to the
database outside of our web UI, our view should contain minimal logic.
"""

import os
import time
import random
import csv

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

from django.shortcuts import render
from person_search import pie, models


# INPROD: ``HAS_MASTERS`` will be set to a tuple: (<percent>, <timestamp>). When
# timestamp gets too old, we re-calculate. This means that every now and then a
# visitor will have their page load slowly. NOT GREAT! A better solutions would
# take time and require some requirements in order to make the best choice. Some
# ideas for production: We are only concerned about this one number, so have a
# separate process (or cluster) that updates the number periodically and writes
# it somewhere (key value store?). The value is updated as necessary
# asynchronously. Visitors just get whatever is the latest value. If we need a
# general solution, using a queue to calculate and store the values
# asynchronously would be something to look into.
HAS_MASTERS = None
HAS_MASTERS_TTL = 600  # how many seconds maximum to we keep the value of
# ``HAS_MASTERS`` before recalculating.

MASTERS_COLOR = 'blue'  # what color our pie slice?


def _get_random_word(length, capitalize=False, length_fuzz=0.2):
    """get a random "word" of approximately ``length``
    """
    max_chomp = length * length_fuzz
    length = random.randint(int(length - max_chomp), length)
    alpha = list('abcdefghijklmnopqrstuvwxyz')
    random.shuffle(alpha)
    word = ''.join(alpha[:length])
    if capitalize:
        word = word.capitalize()
    return word


def show_pie(request):

    global HAS_MASTERS

    # we might want to catch an exception here and return a 500
    total = len(models.Person.objects.all())

    if total == 0:
        percent = 0  # we would otherwise wind up calculating 0/0
    else:
        if HAS_MASTERS is None or time.time() - HAS_MASTERS[1] > HAS_MASTERS_TTL:
            logger.debug('[re]calculating "HAS_MASTERS"...')
            # INPROD: There are probably faster ways of doing this:
            count = len([p for p in models.Person.objects.all()
                         if p.degree and p.degree.is_masters()])
            HAS_MASTERS = (count, time.time())
        percent = HAS_MASTERS[0] / total * 100.0
    context = {
        'pie_chart': pie.get_pie(round(percent), MASTERS_COLOR),
        'total_persons': total,
        'with_masters': 0 if HAS_MASTERS is None else HAS_MASTERS[0],
        'percent_with_masters': '%.3g' % percent,
        'masters_color': MASTERS_COLOR,
    }
    return render(request, 'pie.html', context)


def person_profile(request, email):
    """Lacking something to scrape (see ``README.md``) we create a "test
    person". If an email address is supplied from the test data, the person with
    that email address is returned from the supplied CSV test data. For unknown
    email addresses, a random (very random) person is returned. No checking of
    the input is done. Even for random user-supplied email addresses, we always
    get the same profile back (use of ``random.seed()``.)
    """
    # INPROD: We wouldn't do anything like this in production!! This is all
    # totally contrived.
    resources = os.path.join(os.path.dirname(__file__), 'resources')
    # WARNING: file i/o !
    with open(os.path.join(resources, 'actual_persons.csv')) as f:
        f.readline()  # discard header row
        for row in csv.reader(f):
            if email.lower().strip() == row[1].lower().strip():
                full_name, _, gender, degree_name, institution = row
                break
        else:
            # ``else`` we create a good-enough random person. For a given email,
            # ``random.seed()`` to its value "as an int". This ensures we
            # consistently get the same person info for a given email.
            i = int.from_bytes(bytes(email, encoding='utf-8'), byteorder='big')
            random.seed(i)
            full_name = '%s %s' % (_get_random_word(7, capitalize=True),
                                   _get_random_word(12, capitalize=True))
            gender = random.choice(['M', 'F'])
            degree_name = random.choice(['MS', 'MA', 'MBA', 'AA', 'BA', 'BS',
                                         'PHD'])
            institution = 'University of %s' % _get_random_word(25,
                                                                capitalize=True)
    context = {
        'full_name': full_name,
        'email': email,
        'gender': gender,
        'degree_name': degree_name,
        'institution': institution,
    }
    return render(request, 'person_profile.html', context)
