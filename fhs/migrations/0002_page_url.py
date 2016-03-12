# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fhs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='url',
            field=models.URLField(default=b'http://medlineplus.com'),
            preserve_default=True,
        ),
    ]
