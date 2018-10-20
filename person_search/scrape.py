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
    degrees = {}
    for i in range(1, 5):
        degrees[i] = db.Degree(name='foo', institution='bar%s' % i)
        degrees[i].save()
    for name, email, degree in [
            ('Mary Blarge', 'mary@example.com', 1),
            ('Zoo Keeper', 'zoo@example.com', 2),
            ('Mr Joe', 'kenm@example.com', 3),
            ('Bob Example', 'bob@example.com', 4),
    ]:
        insertions.append(db.Person(full_name=name, email=email, degree=degrees[degree]))
    # NOTE: `.save()` done by django orm after `bulk_create`
    db.Person.objects.bulk_create(insertions)

def main():
    script_basename, _ = os.path.splitext(os.path.basename(__file__))


if __name__ == '__main__':
    writethings()
    readthing()
