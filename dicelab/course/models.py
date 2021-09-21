from django.db import models

# Create your models here.


class Course(models.Model):
    code = models.CharField(max_length=10, null=False, default='')
    name = models.CharField(max_length=100, null=False, default='')
    semester = models.CharField(max_length=200, null=False, default='')
