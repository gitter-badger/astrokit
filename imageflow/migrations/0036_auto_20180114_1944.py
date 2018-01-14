# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2018-01-14 19:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imageflow', '0035_auto_20171210_1648'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reduction',
            name='second_order_extinction',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='reduction',
            name='tf',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='reduction',
            name='tf_graph_url',
            field=models.CharField(max_length=1024, null=True),
        ),
    ]
