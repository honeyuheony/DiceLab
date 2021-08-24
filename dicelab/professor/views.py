from django.shortcuts import render
from .tasks import *
from django.core.cache import cache


load_init_data = False

# Create your views here.


def professor(request):
    global load_init_data
    if load_init_data:
        page = cache.get('page')
        set_cache.delay()
    else:
        load_init_data = True
        page = cache.set(
            'page', load_notionAPI_professor()['body'])
        page = cache.get('page')
    return render(request, 'professor.html', {'page': page})
