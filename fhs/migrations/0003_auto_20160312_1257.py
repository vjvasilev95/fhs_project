# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fhs', '0002_page_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='flesch_score',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='page',
            name='sentiment_score',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='page',
            name='subjectivity_score',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='page',
            name='summary',
            field=models.TextField(default=b'test'),
        ),
    ]
