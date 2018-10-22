# -*- mode: python; coding: utf-8 -*-
"""A straightforward function-based view. Since we read and write to the database outside of our web UI, our view should contain minimal logic.
"""

import time
from django.shortcuts import render
from person_search import pie, models

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# INPROD: ``HAS_MASTERS`` will be set to a tuple: (<percent>, <timestamp>). When timestamp gets too old, we re-calculate. This means that every now and then a visitor will have their page load slowly. NOT GREAT! A better solutions would take time and require some requirements in order to make the best choice. Some ideas for production: We are only concerned about this one number, so have a separate process (or cluster) that updates the number periodically and writes it somewhere (key value store?). The value is updated as necessary asyncronously. Visitors just get whatever is the latest value. If we need a general solution, using a queue to calculate and store the values asyncronously would be something to look into.
HAS_MASTERS = None
HAS_MASTERS_TTL = 600  # how many seconds maximum to we keep the value of ``HAS_MASTERS`` before recalculating.

def index(request):

    global HAS_MASTERS

    # we might want to catch an exception here and return a 500
    total = len(models.Person.objects.all())

    if total == 0:
        percent = 0  # we would otherwise wind up calculating 0/0
    else:
        if HAS_MASTERS is None or time.time() - HAS_MASTERS[1] > HAS_MASTERS_TTL:
            logger.debug('[re]calculating "HAS_MASTERS"...')
            # INPROD: There are probably faster ways of doing this:
            count = len([p for p in models.Person.objects.all() if p.degree.is_masters()])
            HAS_MASTERS = (count, time.time())
        percent =  HAS_MASTERS[0] / total * 100.0
    context = {'pie_chart': pie.get_pie(int(percent))}
    return render(request, 'person_search.html', context)
