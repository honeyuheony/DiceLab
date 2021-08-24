from django.shortcuts import render
from .tasks import *
from django.core.cache import cache


# Create your views here.
load_init_data = False


def member(request):
    global load_init_data
    if load_init_data:
        graduate = cache.get('graduate')
        ungraduate = cache.get('ungraduate')
        urp = cache.get('urp')
        alumni = cache.get('alumni')

        set_cache.delay()
    else:
        load_init_data = True
        cache.set(
            'graduate', load_notionAPI_member_graduate()['body'])
        graduate = cache.get('graduate')
        cache.set(
            'ungraduate', load_notionAPI_member_ungraduate()['body'])
        ungraduate = cache.get('ungraduate')
        cache.set('urp', load_notionAPI_member_urp()['body'])
        urp = cache.get('urp')
        cache.set('alumni', load_notionAPI_member_alumni()['body'])
        alumni = cache.get('alumni')

    return render(request, 'member.html', {
        'graduate': graduate, 'ungraduate': ungraduate, 'urp': urp, 'alumni': alumni})
