# Generated by Django 3.2.6 on 2022-01-12 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0004_alter_graduated_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='alumni',
            name='project',
            field=models.ManyToManyField(related_name='project', to='member.Project'),
        ),
    ]
