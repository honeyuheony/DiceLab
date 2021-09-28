from django.db import models

# Create your models here.


class Research_interests(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=20, null=False)

    def __str__(self):
        return self.title


class Linked(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=20, null=False)
    link = models.CharField(max_length=500, null=False)

    def __str__(self):
        return self.title


class Graduated(models.Model):
    name = models.CharField(max_length=10, null=False)
    course = models.CharField(max_length=30, null=False)
    admission_date = models.CharField(max_length=10, null=False)
    research_interests = models.ManyToManyField(
        Research_interests, related_name='research_interests')
    email = models.CharField(max_length=30, null=False)
    pic = models.CharField(max_length=20, null=False)
    linked = models.ManyToManyField(Linked, related_name='linked')

    def __str__(self):
        return self.name


class Team(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class Alumni(models.Model):
    name = models.CharField(primary_key=True, max_length=10, null=False)
    course = models.CharField(max_length=30, null=False)
    team = models.ManyToManyField(Team, related_name='team')
    graduate_year = models.CharField(max_length=10, null=False)

    def __str__(self):
        return self.name
