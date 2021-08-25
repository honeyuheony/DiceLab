from django.shortcuts import render
from .tasks import *
from django.core.cache import cache

load_init_data = False

def project(request):
    global load_init_data
    if load_init_data:
        projects = cache.get('project')
        ai_challenges = cache.get('ai_challenge')

        set_cache.delay()
    else:
        load_init_data = True
        cache.set('project', load_notionAPI_project()['body'])
        cache.set(
            'ai_challenge', load_notionAPI_ai_challenge()['body'])
        projects = cache.get('project')
        ai_challenges = cache.get('ai_challenge')
    return render(request, 'project.html', {'projects': projects, 'ai_challenges': ai_challenges})
