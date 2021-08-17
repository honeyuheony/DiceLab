from django.urls import path
from .views import *
urlpatterns = [
    path('', professor, name="professor"),
]