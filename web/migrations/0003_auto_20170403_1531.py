# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-04-03 15:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_auto_20170329_2122'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='custom_field',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='profile_photo',
            field=models.FileField(null=True, upload_to='uploads/'),
        ),
    ]
