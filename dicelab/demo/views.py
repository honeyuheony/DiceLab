from django.shortcuts import render
from .models import Demo
import json
from .tasks import *

# Create your views here.


def demo(request):
    # set_data()
    demo = Demo.objects.all().order_by('-date')
    demo_list = []
    for n in demo:
        temp = {}
        temp['title'] = n.title
        temp['date'] = n.date
        temp['description'] = n.description
        temp['video'] = n.video
        demo_list.append(temp)
    return render(request, 'demo.html', {'demo': demo_list})
