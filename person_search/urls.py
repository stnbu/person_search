"""Thinking of this as a Django "app", this file should be minimal. TBD in production.
"""

from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', RedirectView.as_view(url='/pie/')),  # a pattern would be better
    path('pie/', views.show_pie, name='pie'),
    path('person_profile/<str:email>/', views.person_profile, name='person_profile')
]

# INPROJ: does not belong here if this is an 'app'
from django.contrib import admin
urlpatterns.append(path('admin/', admin.site.urls))
