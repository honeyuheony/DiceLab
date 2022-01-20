from django.db import models


class Research_interests(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class Linked(models.Model):
    title = models.CharField(max_length=20)
    link = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.title


class Graduated(models.Model):
    name = models.CharField(max_length=20)
    course = models.CharField(max_length=30, blank=True)
    admission_date = models.CharField(max_length=10, blank=True)
    research_interests = models.ManyToManyField(
        Research_interests, related_name='graduated', blank=True)
    email = models.CharField(max_length=30, blank=True)
    pic = models.CharField(max_length=20, blank=True)
    linked = models.ManyToManyField(
        Linked, related_name='graduated', blank=True)

    def __str__(self):
        return self.name


class Team(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class Project(models.Model):
    title = models.CharField(max_length=40)
    year = models.CharField(max_length=10, null=True)

    def __str__(self):
        return self.title


class Master(models.Model):
    name = models.CharField(max_length=20)
    graduate_year = models.CharField(max_length=10, blank=True)
    research_interests = models.ManyToManyField(
        Research_interests, related_name='master', blank=True)
    email = models.CharField(max_length=30, blank=True)
    pic = models.CharField(max_length=20, blank=True)
    paper = models.CharField(max_length=50, blank=True)
    linked = models.ManyToManyField(
        Linked, related_name='master', blank=True)

    def __str__(self):
        return self.name


class Alumni(models.Model):
    name = models.CharField(max_length=10)
    course = models.CharField(max_length=30, blank=True)
    team = models.ManyToManyField(Team, related_name='alumni')
    graduate_year = models.CharField(max_length=10, null=True)
    project = models.ManyToManyField(
        Project, related_name='alumni', blank=True)

    def __str__(self):
        return self.name
