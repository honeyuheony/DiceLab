from django.urls import path
from .views import *
urlpatterns = [
    path('', seminal, name="seminal"),
]
