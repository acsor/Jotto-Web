# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-12 14:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('JottoWebApp', '0002_auto_20170812_1319'),
    ]

    operations = [
        migrations.RenameField(
            model_name='guess',
            old_name='guess',
            new_name='name',
        ),
    ]
