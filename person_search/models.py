# -*- mode: python; coding: utf-8 -*-

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

from django.db import models
from person_search.crypto import crypt13 as crypt


class EncryptedCharField(models.CharField):

    def from_db_value(self, value, expression, connection, context):  # DECRYPT
        logger.debug('calling from_db_value with `%s`' % value)
        return crypt(value, decrypt=True)

    def get_prep_value(self, value):  # ENCRYPT
        logger.debug('calling get_prep_value with `%s`' % value)
        return crypt(value, decrypt=False)


class Persons(models.Model):

    email = EncryptedCharField(db_index=True, max_length=100)
    full_name = EncryptedCharField(max_length=200)

    def __str__(self):
        return '%s <%s>' % (self.full_name, self.email)

    class Meta:
        app_label = 'person_search'  # needed by db.py
