"""Thinking of this as a Django "app", this file should be minimal. TBD in production.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]

# INPROJ: does not belong here if this is an 'app'
from django.contrib import admin
urlpatterns.append(path('admin/', admin.site.urls))
