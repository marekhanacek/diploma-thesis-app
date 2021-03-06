# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-04-25 08:52
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('web', '0011_feedback_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='user_responded',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='feedbacks_responded', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
