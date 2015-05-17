# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diad', '0003_auto_20150514_0155'),
    ]

    operations = [
        migrations.RenameField(
            model_name='album',
            old_name='portada',
            new_name='url',
        ),
        migrations.RenameField(
            model_name='fotos',
            old_name='imagen',
            new_name='url',
        ),
    ]
