from django.shortcuts import render
from .tasks import *

# Create your views here.
load_init_data = False

def news(request):
    global load_init_data
    if load_init_data:
        news = cache.get('news')
        set_cache.delay()
    else:
        load_init_data = True
        news = cache.set(
            'news', load_notionAPI_news()['body'])
        news = cache.get('news')
    return render(request, 'news.html', {'news': news})