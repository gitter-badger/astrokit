# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2017-06-25 21:48
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imageflow', '0012_auto_20170625_2115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='analysisresult',
            name='image_datetime',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2017, 6, 25, 21, 48, 44, 458335)),
            preserve_default=False,
        ),
    ]