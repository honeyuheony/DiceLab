from django.db import models

# Create your models here.


class Professor_Page_Code(models.Model):
    image = models.CharField(max_length=100)
    body = models.CharField(max_length=100000000000)
    create_date = models.DateTimeField('Created_date', auto_now_add=True)
