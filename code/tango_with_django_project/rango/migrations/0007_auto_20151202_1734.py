# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0006_auto_20151202_1732'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='user1',
            new_name='user',
        ),
    ]
