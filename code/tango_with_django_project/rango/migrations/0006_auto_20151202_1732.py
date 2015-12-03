# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0005_userprofile_test_field'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='user',
            new_name='user1',
        ),
    ]
