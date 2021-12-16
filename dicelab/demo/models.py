from django.db import models


class Demo(models.Model):
    title = models.CharField(primary_key=True, max_length=50)
    description = models.CharField(max_length=500)
    video = models.CharField(max_length=50)
    date = models.CharField(max_length=10)

    def __str__(self):
        return self.title
