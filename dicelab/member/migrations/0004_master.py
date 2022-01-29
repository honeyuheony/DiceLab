# Generated by Django 3.2.6 on 2022-01-20 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0003_project_year'),
    ]

    operations = [
        migrations.CreateModel(
            name='Master',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('course', models.CharField(blank=True, max_length=30)),
                ('graduate_year', models.CharField(blank=True, max_length=10)),
                ('email', models.CharField(blank=True, max_length=30)),
                ('pic', models.CharField(blank=True, max_length=20)),
                ('paper', models.CharField(blank=True, max_length=50)),
                ('linked', models.ManyToManyField(blank=True, related_name='master', to='member.Linked')),
                ('research_interests', models.ManyToManyField(blank=True, related_name='master', to='member.Research_interests')),
            ],
        ),
    ]