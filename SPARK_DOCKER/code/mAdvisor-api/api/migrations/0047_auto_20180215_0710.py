# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-02-15 07:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0046_merge_20180208_0707'),
    ]

    operations = [
        migrations.AddField(
            model_name='score',
            name='live_status',
            field=models.CharField(choices=[('0', 'Not Started Yet'), ('1', 'Signal Creation Started.'), ('2', 'Trend Created'), ('3', 'ChiSquare Created'), ('4', 'Decision Tree Created'), ('5', 'Density Histogram Created'), ('6', 'Regression Created'), ('7', 'Signal Creation Done')], default='0', max_length=300),
        ),
        migrations.AddField(
            model_name='score',
            name='viewed',
            field=models.BooleanField(default=False),
        ),
    ]
