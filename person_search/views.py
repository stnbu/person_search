"""A straightforward function-based view. Since we read and write to the database outside of our web UI, our view should contain minimal logic.
"""

from django.shortcuts import render

def index(request):
    context = {}
    return render(request, 'person_search.html', context)
