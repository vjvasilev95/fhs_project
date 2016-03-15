# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fhs', '0004_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='shared',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
