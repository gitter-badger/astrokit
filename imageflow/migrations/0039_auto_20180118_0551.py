# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2018-01-18 05:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imageflow', '0038_auto_20180114_2035'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AnalysisResult',
            new_name='ImageAnalysis',
        ),
    ]
