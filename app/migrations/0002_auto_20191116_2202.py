# Generated by Django 2.2.6 on 2019-11-16 16:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='professor',
            name='name',
        ),
        migrations.RemoveField(
            model_name='student',
            name='name',
        ),
    ]
