# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-23 17:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diad', '0005_auto_20170523_1227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='url',
            field=models.ImageField(max_length=250, upload_to=b'diad/static/img/portada'),
        ),
    ]
