# Generated by Django 4.0.2 on 2022-02-21 07:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='visit',
            name='computername',
        ),
        migrations.RemoveField(
            model_name='visit',
            name='username',
        ),
    ]