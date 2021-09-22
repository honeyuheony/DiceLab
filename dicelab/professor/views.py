from django.shortcuts import render
from .tasks import *


def professor(request):
    page = set_data()
    return render(request, 'professor.html', {'page': page})
