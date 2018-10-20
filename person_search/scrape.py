# -*- mode: python; coding: utf-8 -*-
"""Scrape!
"""

from person_search import db


def readthing(self, thing):
    try:
        last_thing = db.Persons.objects.filter(
            thing=thing).order_by('id').latest()
    except db.Persons.DoesNotExist:
        pass


def writethings(self, thing, data):
    insertions = []
    for row in data:
        insertions.append(db.Persons(thing=thing, **row))
    # NOTE: `.save()` done by django orm after `bulk_create`
    db.Persons.objects.bulk_create(insertions)


def main():
    script_basename, _ = os.path.splitext(os.path.basename(__file__))


if __name__ == '__main__':
    main()
