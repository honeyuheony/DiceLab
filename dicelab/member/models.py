from django.db import models


class Research_interests(models.Model):
    title = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.title


class Linked(models.Model):
    title = models.CharField(max_length=20, null=True)
    link = models.CharField(max_length=500, null=True)

    def __str__(self):
        return self.title


class Graduated(models.Model):
    name = models.CharField(max_length=10, null=True)
    course = models.CharField(max_length=30, null=True)
    admission_date = models.CharField(max_length=10, null=True)
    research_interests = models.ManyToManyField(
        Research_interests, related_name='research_interests')
    email = models.CharField(max_length=30, null=True)
    pic = models.CharField(max_length=20, null=True)
    linked = models.ManyToManyField(Linked, related_name='linked')

    def __str__(self):
        return self.name


class Team(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class Alumni(models.Model):
    name = models.CharField(max_length=10, default='username')
    course = models.CharField(max_length=30, null=True)
    team = models.ManyToManyField(Team, related_name='team')
    graduate_year = models.CharField(max_length=10, null=True)

    def __str__(self):
        return self.name
