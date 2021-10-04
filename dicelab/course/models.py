from django.db import models

# Create your models here.


class Semester(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=20, blank=True)
    year = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.year + " " + self.title


class Course(models.Model):
    code = models.CharField(max_length=10, default='', primary_key=True)
    name = models.CharField(max_length=100, blank=False, default='')
    semester = models.ManyToManyField(
        Semester, related_name='semester')

    def __str__(self):
        return self.name
