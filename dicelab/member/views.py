from django.shortcuts import render
from .tasks import *
from .models import *


def member(request):
    # set_data()
    graduated = Graduated.objects.all().order_by(
        '-course', 'admission_date', 'name')
    alumni = Alumni.objects.all()
    return render(request, 'member.html', {'graduated': graduated, 'alumni': alumni})
