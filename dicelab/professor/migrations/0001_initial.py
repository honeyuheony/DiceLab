# Generated by Django 3.2.6 on 2022-01-29 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Professor_Page_Code',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.CharField(max_length=100)),
                ('body', models.CharField(max_length=100000000000)),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Created_date')),
            ],
        ),
    ]
