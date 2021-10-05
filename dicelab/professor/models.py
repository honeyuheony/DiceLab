from django.db import models
from django.db.models.fields import CharField
from django.db.models.fields.related import ManyToManyField

# Create your models here.


class Professor(models.Model):
    name = CharField(max_length=30)


class Introduction(models.Model):
    position = CharField(max_length=30, null=True)
    affiliation = CharField(max_length=30, null=True)


class Contact(models.Model):
    location = CharField(max_length=30, null=True)
    email = CharField(max_length=30, null=True)


class Interest(models.Model):
    field = CharField(max_length=30, null=True)


class Research_interests(models.Model):
    interest = ManyToManyField(Interest)
