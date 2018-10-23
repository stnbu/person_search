# -*- mode: python; coding: utf-8 -*-
"""Django database model classes.

* ``Person`` -- Stores persons scraped from the web, all data encrypted here.
* ``Degree`` -- A "degree name", institution tuple. A foreign key lets us assign
(a single) degree to each person.

Encryption is seamlessly performed here using custom Django fields.
"""

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

from django.db import models
#from person_search.crypto import crypt
# INPROD: In production we would use postgres-level encryption. See
# ``README.md``
from person_search.crypto import crypt13 as crypt


class EncryptedCharField(models.CharField):
    """An encrypted ``CharField``
    """
    def from_db_value(self, value, expression, connection, context):  # DECRYPT
        logger.debug('calling from_db_value with `%s`' % value)
        return self.to_python(value)

    def to_python(self, value):
        logger.debug('calling to_python with `%s`' % value)
        if not value:
            return value
        value = crypt(value, decrypt=True)
        return super(EncryptedCharField, self).to_python(value)

    def get_prep_value(self, value):  # ENCRYPT
        logger.debug('calling get_prep_value with `%s`' % value)
        if not value:
            return value
        return crypt(value, decrypt=False)

class EncryptedLowerCharField(EncryptedCharField):
    """An encrypted ``CharField`` where values are always lower-cased before
    encryption (see remark about encryption in ``README.md``)
    """
    def get_prep_value(self, value):  # ENCRYPT
        logger.debug('calling get_prep_value with `%s`' % value)
        value = value.lower()
        return super(EncryptedLowerCharField, self).get_prep_value(value)

class Degree(models.Model):

    name = models.CharField(max_length=20, blank=False)
    institution = models.CharField(max_length=200, blank=False)

    def is_masters(self):
        """Using available information about the ``Degree``, return ``True`` if
        master's degree.
        """
        # Of course this is a ridiculous implementation. It's hard to know
        # without more information. Perhaps have a "master list" of regular
        # expressions, where any match on the contents of the ``name`` column
        # (the name of the degree, BS, etc) constitutes "is masters". Lots of
        # possibilities. This works for our PoC.
        return 'M' in self.name

    def __str__(self):
        return '%s, %s' % (self.name, self.institution)

    class Meta:
        app_label = 'person_search'  # needed by db.py
        unique_together = (('name', 'institution'),)

class Person(models.Model):
    """The column widths are over-spec'd here to account for encoding overhead.
    See ``README.md``
    """

    full_name = EncryptedCharField(max_length=200, blank=False)
    # INPROD: for simplicity, one email per person
    email = EncryptedLowerCharField(db_index=True, max_length=100, unique=True,
                                    blank=False)
    gender = EncryptedCharField(db_index=True, max_length=10, blank=True)
    # INPROD: for simplicity one degree per person. Note that this is not
    # encrypted. PostgreSQL level encryption was the way to go. See
    # ``README.md``
    degree = models.ForeignKey(Degree, on_delete=models.CASCADE, null=True,
                               blank=True)  # null=True - person without degree

    def __str__(self):
        return '%s <%s>' % (self.full_name, self.email)

    class Meta:
        app_label = 'person_search'  # needed by db.py
        unique_together = (('full_name', 'email', 'degree'))
