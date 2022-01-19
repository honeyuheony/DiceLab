from django.shortcuts import render
from .tasks import *
from .models import *


def member(request):
    # set_data()
    alumni = {}
    year = [2020, 2021, 2022, 2023]

    graduated = Graduated.objects.all().order_by(
        '-course', 'admission_date', 'name')
    project_4th = Project.objects.filter(year=year[-2])
    project_3th = Project.objects.filter(year=year[-1])

    for y in year:
        target = {}
        target['member'] = Alumni.objects.filter(
            graduate_year=y).order_by('project', '-course')
        alumni[y] = target
    # print(alumni)

    return render(request, 'member.html', {'graduated': graduated, 'alumni': alumni, 'project_4th': project_4th, 'project_3th': project_3th})
