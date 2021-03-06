# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-03-16 12:35
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('identificator', models.CharField(max_length=3)),
                ('prefix', models.CharField(max_length=10)),
                ('postfix', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=50)),
                ('stars', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lat', models.FloatField()),
                ('lng', models.FloatField()),
                ('radius', models.FloatField()),
                ('amount', models.IntegerField()),
                ('exchange_rate', models.FloatField()),
                ('comment', models.CharField(max_length=250)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('currency_from', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='offers_from', to='web.Currency')),
                ('currency_to', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='offers_to', to='web.Currency')),
            ],
        ),
        migrations.CreateModel(
            name='OfferStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='offer',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='web.OfferStatus'),
        ),
        migrations.AddField(
            model_name='offer',
            name='user_created',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='created_offers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='offer',
            name='user_responded',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='responded_offers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='feedback',
            name='offer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedbacks', to='web.Offer'),
        ),
        migrations.AddField(
            model_name='feedback',
            name='user_created',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='feedbacks_created', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='feedback',
            name='user_responded',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='feedbacks_responded', to=settings.AUTH_USER_MODEL),
        ),
    ]
