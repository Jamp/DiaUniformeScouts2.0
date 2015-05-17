# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diad', '0002_auto_20150514_0146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='portada',
            field=models.ImageField(upload_to=b'diad/static/img/portada/%Y'),
        ),
        migrations.AlterField(
            model_name='fotos',
            name='imagen',
            field=models.ImageField(upload_to=b'diad/static/img/album/%Y'),
        ),
    ]
