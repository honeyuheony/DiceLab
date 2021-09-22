from django.shortcuts import render
from .tasks import *
from .models import News

# Create your views here.

def news(request):
    set_data()
    news = News.objects.all().order_by('-date')
    return render(request, 'news.html', {'news': news})