from django.shortcuts import render
from .tasks import *
from django.core.cache import cache

load_init_data = False


def publication(request):
    global load_init_data
    if load_init_data:
        publication = cache.get('publication')
        patents = cache.get('patent')

        set_cache.delay()
    else:
        load_init_data = True
        cache.set('publication', load_notionAPI_publication()['body'])
        cache.set('patent', load_notionAPI_patents()['body'])

        publication = cache.get('publication')
        patents = cache.get('patent')
    return render(request, 'publication.html', {'publication': publication, 'patents': patents})
