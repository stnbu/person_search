from django.db import models

class Persons(models.Model):

    foo = models.CharField(db_index=True, max_length=100)
    bar = models.FloatField()
    baz = models.IntegerField()

    @property
    def person(self):
        return getattr(self, 'foo')

    @person.setter
    def person(self, value):
        setattr(self, THE_PRICE_FIELD, value)
        
    def __str__(self):
        class_name = self.__class__.__name__
        return '{}@{}'.format(
            self.dt,
            self.person
        )

    class Meta:
        app_label = 'person_search'
        get_latest_by = 'id'
