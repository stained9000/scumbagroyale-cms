# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-07-06 20:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clanwar', '0014_arenas_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='players',
            name='rank',
            field=models.IntegerField(default=0, null=True),
        ),
    ]