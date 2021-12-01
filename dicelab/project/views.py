from django.shortcuts import render
from .tasks import set_data
from .models import AI_challenge, Project


def project(request):
    set_data()
    projects = Project.objects.order_by('-date')
    ai_challenges = AI_challenge.objects.order_by('-date')

    return render(request, 'project.html', {'projects': projects, 'ai_challenges': ai_challenges})
