# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2018-02-01 06:28
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('imageflow', '0004_auto_20180130_0340'),
    ]

    operations = [
        migrations.AddField(
            model_name='imageanalysis',
            name='image_unknown_stars',
            field=jsonfield.fields.JSONField(default={}),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='imageanalysis',
            name='image_unknown_stars_json_url',
            field=models.CharField(default='{}', max_length=1024),
            preserve_default=False,
        ),
    ]
