# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diad', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='album',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='album',
            name='portada',
            field=models.ImageField(upload_to=b'static/img/portada/%Y'),
        ),
        migrations.AlterField(
            model_name='fotos',
            name='album',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='fotos',
            name='imagen',
            field=models.ImageField(upload_to=b'static/img/album/%Y'),
        ),
    ]
