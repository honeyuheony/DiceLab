from django.contrib import admin
from .models import Dissertation, Master, Research_interests, Linked, Graduated, Alumni, Team, Project
# Register your models here.

admin.site.register(Research_interests)
admin.site.register(Linked)
admin.site.register(Dissertation)
admin.site.register(Graduated)
admin.site.register(Alumni)
admin.site.register(Team)
admin.site.register(Project)
admin.site.register(Master)
