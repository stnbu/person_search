from django.contrib import admin
from .models import Person, Email, Institution, Degree

admin.site.register(Person)
admin.site.register(Email)
admin.site.register(Institution)
admin.site.register(Degree)
