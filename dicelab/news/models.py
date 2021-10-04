from django.db import models

# Create your models here.


class News(models.Model):
    title = models.CharField(max_length=100, default='', primary_key=True)
    date = models.CharField(max_length=10)
    htmldata = models.CharField(max_length=1000)

    def __str__(self):
        return self.title
