from django.shortcuts import render
from .tasks import *
from .models import *


def member(request):
    set_data()
    graduated = Graduated.objects.all()
    alumni = Alumni.objects.all()
    return render(request, 'member.html', {'graduated': graduated, 'alumni': alumni})
