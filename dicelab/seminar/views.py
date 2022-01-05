from django.shortcuts import render
from .models import Seminar
from .tasks import set_data
from django.db.models import Q


def seminar(request):
    set_data()
    seminar = Seminar.objects.order_by('-date')
    search_key = request.GET.get('key', '')
    search_type = 'all'
    if search_key:
        if len(search_key) > 1:
            if search_type == 'all':
                seminar = seminar.filter(
                    Q(title__icontains=search_key) | Q(date__icontains=search_key) | Q(speaker__icontains=search_key) | Q(source__icontains=search_key) | Q(year__icontains=search_key) | Q(area__icontains=search_key) | Q(paper__icontains=search_key))
    return render(request, 'seminar.html', {'seminar': seminar})
