from django.shortcuts import render
from .tasks import *
from .models import *


def school(request):
    set_data()
    school = School.objects.order_by('-title')
    return render(request, 'school.html', {'school': school})
