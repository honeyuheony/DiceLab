# Generated by Django 3.2.6 on 2022-01-29 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Semester',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=20)),
                ('year', models.CharField(blank=True, max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('code', models.CharField(blank=True, default='', max_length=10)),
                ('name', models.CharField(default='', max_length=100, primary_key=True, serialize=False)),
                ('semester', models.ManyToManyField(related_name='semester', to='course.Semester')),
            ],
        ),
    ]
