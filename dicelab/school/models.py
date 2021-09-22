from django.db import models


class Lecture(models.Model):
    name = models.CharField(primary_key=True, max_length=50)
    url = models.URLField()

    def __str__(self):
        return self.name


class School(models.Model):
    title = models.CharField(primary_key=True, max_length=50,)
    lecture = models.ManyToManyField(Lecture)

    def __str__(self):
        return self.title
