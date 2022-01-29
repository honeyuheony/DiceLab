from traceback import print_tb
from django.shortcuts import render
from .tasks import *
from .models import Professor_Page_Code
import json


def professor(request):
    set_data()
    db = Professor_Page_Code.objects.all()
    page = eval(db.values('body')[0]['body'])
    return render(request, 'professor.html', {'page': page})
