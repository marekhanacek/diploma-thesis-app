# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-04-07 09:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0005_auto_20170405_1700'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='email',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='phone',
            field=models.CharField(default='', max_length=255),
        ),
    ]
