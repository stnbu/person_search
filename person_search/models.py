from django.db import models

class EncryptedCharField(models.CharField):
    pass

class Persons(models.Model):

    email = EncryptedCharField(db_index=True, max_length=100)
    full_name = EncryptedCharField(max_length=200)

    def __str__(self):
        return '%s <%s>' % (self.full_name, self.email)

    class Meta:
        app_label = 'person_search'  # needed by db.py
