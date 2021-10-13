from django.shortcuts import render
from .tasks import *
from .models import News
import json


def news(request):
    set_data()
    news = News.objects.all().order_by('-date')
    news_list = []
    for n in news:
        temp = {}
        temp['title'] = n.title
        temp['date'] = n.date
        temp['content'] = json.decoder.JSONDecoder().decode(n.content)
        temp['pic'] = n.pic
        news_list.append(temp)
    return render(request, 'news.html', {'news': news_list})
