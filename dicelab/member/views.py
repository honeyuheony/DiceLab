from django.shortcuts import render
from datetime import datetime
from django.db.models import Case, Q, When
from .tasks import *
from .models import *


def member(request):
    # set_data()
    current_year = datetime.now().year + 1
    year = [current_year-x for x in range(current_year - 2020 + 1)]
    print(year)
    course_list = ['Ph.D. course', 'M.S.-Ph.D. integrated course',
                   'B.S.-M.S. integrated', 'M.S. course']
    project = {}
    preserved = Case(*[When(course=course, then=pos)
                     for pos, course in enumerate(course_list)])
    graduated = Graduated.objects.all().order_by(
        preserved, 'admission_date', 'name')
    project_4th = Project.objects.filter(year=year[1])
    project_3th = Project.objects.filter(year=year[0])
    for y in year:
        project[y] = Project.objects.filter(year=y)
    master = Master.objects.all().order_by('graduate_year', '-name')
    no_project_alumni = Alumni.objects.filter(
        project=None, graduate_year=2020).order_by('graduate_year')

    return render(request, 'member.html', {'graduated': graduated, 'project_4th': project_4th, 'project_3th': project_3th, 'project': project, 'master': master, 'no_project_alumni': no_project_alumni})
