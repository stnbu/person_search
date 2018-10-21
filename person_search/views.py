"""A straightforward function-based view. Since we read and write to the database outside of our web UI, our view should contain minimal logic.
"""

from django.shortcuts import render
from person_search import pie

def index(request):
    context = {'pie_chart': pie.get_pie(38)}
    return render(request, 'person_search.html', context)
