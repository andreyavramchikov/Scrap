# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-29 14:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('selen', '0003_tripadvisorhotel_done'),
    ]

    operations = [
        migrations.CreateModel(
            name='TripAdvisorHotelInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('url', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('image_url', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=255)),
                ('website', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('done', models.BooleanField(default=False)),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='selen.TripAdvisorHotel')),
            ],
        ),
    ]
