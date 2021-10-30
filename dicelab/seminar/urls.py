from django.urls import path
from .views import *
urlpatterns = [
    path('', seminar, name="seminar"),
]
