from django.shortcuts import render
from .tasks import *
from .models import *


def course(request):
    # set_data()
    semesters = Semester.objects.order_by('-year')
    courses = Course.objects.all()
    return render(request, 'course.html', {'semesters': semesters, 'courses': courses})
