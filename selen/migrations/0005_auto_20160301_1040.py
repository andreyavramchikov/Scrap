# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-01 10:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('selen', '0004_tripadvisorhotelinfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='tripadvisorhotelinfo',
            name='city',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='tripadvisorhotelinfo',
            name='postal',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='tripadvisorhotelinfo',
            name='state',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='tripadvisorhotelinfo',
            name='address',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='tripadvisorhotelinfo',
            name='email',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='tripadvisorhotelinfo',
            name='image_url',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='tripadvisorhotelinfo',
            name='name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='tripadvisorhotelinfo',
            name='phone',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='tripadvisorhotelinfo',
            name='url',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='tripadvisorhotelinfo',
            name='website',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
