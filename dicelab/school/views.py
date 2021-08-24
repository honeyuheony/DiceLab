from django.shortcuts import render
from .tasks import *
from django.core.cache import cache

load_init_data = False
# Create your views here.


def school(request):
    global load_init_data
    if load_init_data:
        school = cache.get('school')
        set_cache.delay()
    else:
        load_init_data = True
        cache.set(
            'school', load_notionAPI_school()['body'])
        school = cache.get('school')

    return render(request, 'school.html', {'school': school})
