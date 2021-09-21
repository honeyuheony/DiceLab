from django.shortcuts import render
from .tasks import set_data
from .models import Patents, Publication


def publication(request):
    set_data()
    publication = Publication.objects.all()
    patents = Patents.objects.all()
    return render(request, 'publication.html', {'publication': publication, 'patents': patents})
