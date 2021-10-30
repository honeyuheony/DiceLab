from django.db import models

# Create your models here.


class Seminar(models.Model):
    title = models.CharField(max_length=50, primary_key=True)
    date = models.CharField(max_length=50, null=True)
    speaker = models.CharField(max_length=50, null=True)
    source = models.CharField(max_length=50, null=True)
    year = models.CharField(max_length=50, null=True)
    area = models.CharField(max_length=50, null=True)
    paper = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.title
