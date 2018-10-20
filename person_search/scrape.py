# -*- mode: python; coding: utf-8 -*-
"""Scrape!
"""

from person_search import db


def readthing(self, thing):
    try:
        last_thing = db.Person.objects.filter(
            thing=thing).order_by('id').latest()
    except db.Person.DoesNotExist:
        pass


def writethings():
    insertions = []
    for name in ['Mary Blarge', 'Zoo Keeper', 'Mr Joe']:
        insertions.append(db.Person(full_name=name))
    # NOTE: `.save()` done by django orm after `bulk_create`
    db.Person.objects.bulk_create(insertions)

def main():
    script_basename, _ = os.path.splitext(os.path.basename(__file__))


if __name__ == '__main__':
    writethings()
