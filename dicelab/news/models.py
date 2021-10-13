from django.db import models

# Create your models here.


class News(models.Model):
    title = models.CharField(max_length=100)
    date = models.CharField(max_length=10)
    column_type = models.CharField(max_length=20, blank=True)
    content = models.CharField(max_length=100, blank=True)
    pic = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.title + self.date
