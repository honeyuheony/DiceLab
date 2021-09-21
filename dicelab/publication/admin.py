from django.contrib import admin
from .models import Patents, Publication

# Register your models here.

admin.site.register(Publication)
admin.site.register(Patents)
