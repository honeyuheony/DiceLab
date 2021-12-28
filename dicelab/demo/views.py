from django.shortcuts import render
from .models import Demo

# Create your views here.


def demo(request):
    demo = Demo.objects.all().order_by('-date')
    return render(request, 'demo.html', {'demo': demo})
