from django.shortcuts import render
from .models import Seminar
from .tasks import set_data


def seminar(request):
    set_data()
    seminar = Seminar.objects.order_by('-date')
    return render(request, 'seminar.html', {'seminar': seminar})
