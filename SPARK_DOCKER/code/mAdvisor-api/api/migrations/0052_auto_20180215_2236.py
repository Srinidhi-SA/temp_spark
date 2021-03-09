# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-02-15 22:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0051_auto_20180215_2229'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dataset',
            options={'ordering': ['-created_at', '-updated_at'], 'permissions': (('view_dataset', 'View dataset'), ('create_dataset', 'Create dataset'), ('rename_dataset', 'Rename dataset'), ('remove_dataset', 'remove dataset'), ('upload_from_file', 'Upload from file'), ('upload_from_mysql', 'Upload from mysql'), ('upload_from_mssql', 'Upload from mssql'), ('upload_from_hana', 'Upload from hana'), ('data_validation', 'Data Validation'), ('subsetting_dataset', 'Subsetting dataset'))},
        ),
    ]
