# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-24 07:24
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0031_auto_20171010_1033'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockDataset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('stock_symbols', models.CharField(blank=True, max_length=500, null=True)),
                ('slug', models.SlugField(max_length=300, null=True)),
                ('auto_update', models.BooleanField(default=False)),
                ('input_file', models.FileField(null=True, upload_to='conceptsfiles')),
                ('meta_data', models.TextField(default='{}')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('deleted', models.BooleanField(default=False)),
                ('bookmarked', models.BooleanField(default=False)),
                ('analysis_done', models.BooleanField(default=False)),
                ('status', models.CharField(default='Not Registered', max_length=100, null=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('job', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Job')),
            ],
            options={
                'ordering': ['-created_at', '-updated_at'],
            },
        ),
    ]
