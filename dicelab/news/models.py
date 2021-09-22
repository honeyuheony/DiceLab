from django.db import models

# Create your models here.

class News(models.Model):
    date = models.CharField(max_length=10, null=False)
    htmldata = models.CharField(max_length=1000, null=False)

    def __str__(self):
        return self.date