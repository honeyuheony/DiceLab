from django.shortcuts import render
from .tasks import *
from .models import *


# Create your views here.
load_init_data = False


def member(request):
    set_data()
    # research_interests = Research_interests.objects.all.order_by('-title')
    # linked = Linked.objects.all()
    graduated = Graduated.objects.all()
    alumni = Alumni.objects.all()
    return render(request, 'member.html', {'graduated': graduated, 'alumni': alumni})
# 'research_interests': research_interests, 'linked': linked, 