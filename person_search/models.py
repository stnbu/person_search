# -*- mode: python; coding: utf-8 -*-

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

from django.db import models
from person_search.crypto import crypt13 as crypt
#from person_search.crypto import crypt


class EncryptedCharField(models.CharField):

    def from_db_value(self, value, expression, connection, context):  # DECRYPT
        logger.debug('calling from_db_value with `%s`' % value)
        return self.to_python(value)

    def to_python(self, value):
        logger.debug('calling to_python with `%s`' % value)
        value = crypt(value, decrypt=True)
        return super(EncryptedCharField, self).to_python(value)

    def get_prep_value(self, value):  # ENCRYPT
        logger.debug('calling get_prep_value with `%s`' % value)
        return crypt(value, decrypt=False)


class Person(models.Model):

    full_name = EncryptedCharField(max_length=200)

    def __str__(self):
        return self.full_name

    class Meta:
        app_label = 'person_search'  # needed by db.py

class Email(models.Model):

    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    address = EncryptedCharField(db_index=True, max_length=100, unique=True)

    def __str__(self):
        return '%s <%s>' % (self.person.full_name, self.address)

    class Meta:
        app_label = 'person_search'  # needed by db.py

class Institution(models.Model):

    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'person_search'  # needed by db.py

class Degree(models.Model):

    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    degree = models.CharField(max_length=200)
    persons = models.ManyToManyField(Person)

    def __str__(self):
        return '%s, %s' % (self.degree, self.institution.name)

    class Meta:
        app_label = 'person_search'  # needed by db.py
        #unique_together = (('institution', 'degree'),)
