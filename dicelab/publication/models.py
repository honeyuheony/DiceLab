from django.db import models

# Create your models here.


class Publication(models.Model):
    title = models.CharField(max_length=50,
                             default='', primary_key=True)
    label = models.CharField(max_length=20, null=True)
    paper_link = models.CharField(max_length=30, null=True)
    thesis = models.CharField(max_length=20, null=True)
    year = models.CharField(max_length=20, null=True)
    assign = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.title


class Patents(models.Model):
    title = models.CharField(max_length=50,
                             default='', primary_key=True)
    country = models.CharField(max_length=20, null=True)
    num = models.CharField(max_length=20, null=True)
    year = models.CharField(max_length=20, null=True)
    assign = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.title
