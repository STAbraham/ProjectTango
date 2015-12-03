# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0004_auto_20151106_1438'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='test_field',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
