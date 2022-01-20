from django.shortcuts import render
from django.db.models import Case, Q
from .tasks import *
from .models import *


def member(request):
    # set_data()
    year = [2020, 2021, 2022, 2023]
    project = {}
    graduated = Graduated.objects.all().order_by(
        '-course', 'admission_date', 'name')
    project_4th = Project.objects.filter(year=year[-2])
    project_3th = Project.objects.filter(year=year[-1])
    for y in year:
        project[y] = Project.objects.filter(year=y)
    master = Master.objects.all().order_by('graduate_year', '-name')
    # alumni_2020 = Alumni.objects.filter(graduate_year="2020").order_by('-team')
    no_project_alumni = Alumni.objects.filter(
        project=None, graduate_year=2020).order_by('graduate_year')
    # print(no_project_alumni)
    return render(request, 'member.html', {'graduated': graduated, 'project_4th': project_4th, 'project_3th': project_3th, 'project': project, 'master': master, 'no_project_alumni': no_project_alumni})
