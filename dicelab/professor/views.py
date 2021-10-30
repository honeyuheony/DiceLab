from django.shortcuts import render
from .tasks import *


def professor(request):
    page = set_data()['body']
    image = set_data()['image']
    return render(request, 'professor.html', {'page': page, 'image' : image})
