from django.shortcuts import render
from .models import Seminal
from .tasks import set_data


def seminal(request):
    set_data()
    seminal = Seminal.objects.order_by('-date')
    return render(request, 'seminal.html', {'semianl': seminal})
