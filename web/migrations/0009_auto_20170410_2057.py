# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-04-10 20:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0008_offer_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='address',
            field=models.CharField(default='', max_length=191),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='address',
            field=models.CharField(default='', max_length=191),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='basic_information',
            field=models.CharField(default='', max_length=191),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='email',
            field=models.CharField(default='', max_length=191),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='phone',
            field=models.CharField(default='', max_length=191),
        ),
    ]
