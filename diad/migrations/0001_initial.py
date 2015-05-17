# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('album', models.IntegerField(max_length=4)),
                ('portada', models.ImageField(upload_to=b'portada/%Y')),
                ('creado_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Fotos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('imagen', models.ImageField(upload_to=b'album/%Y')),
                ('album', models.IntegerField(max_length=4)),
                ('autorizado', models.BooleanField(default=False)),
                ('creado_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
