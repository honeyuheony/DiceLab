from django.urls import path
from .views import *
urlpatterns = [
    path('', course, name="course"),
]
