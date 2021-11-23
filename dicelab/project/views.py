from django.shortcuts import render
from .tasks import set_data
from .models import AI_challenge, Project


def project(request):
    # set_data()
    projects = Project.objects.all()
    ai_challenges = AI_challenge.objects.all()

    return render(request, 'project.html', {'projects': projects, 'ai_challenges': ai_challenges})
