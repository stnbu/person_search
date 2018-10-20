# -*- mode: python; coding: utf-8 -*-
"""Scrape!
"""

from person_search import db


def readthing():
    print(db.Person.objects.filter(full_name__icontains='%'))
    print(db.Person.objects.filter(full_name='Bob Example'))
    print(db.Person.objects.all())


def writethings():
    insertions = []
    for name in ['Mary Blarge', 'Zoo Keeper', 'Mr Joe', 'Bob Example']:
        insertions.append(db.Person(full_name=name))
    # NOTE: `.save()` done by django orm after `bulk_create`
    db.Person.objects.bulk_create(insertions)

def main():
    script_basename, _ = os.path.splitext(os.path.basename(__file__))


if __name__ == '__main__':
    writethings()
    readthing()
