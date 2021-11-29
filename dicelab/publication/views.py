from django.shortcuts import render
from .tasks import set_data
from .models import Patents, Publication


def publication(request):
    set_data()
    publication = Publication.objects.order_by('-year')
    patents = Patents.objects.order_by('-year')
    return render(request, 'publication.html', {'publication': publication, 'patents': patents})
