# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-07-09 15:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clanwar', '0017_arenas_max_trophy_limit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='arenas',
            name='force_quest_chest_cycle',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='arenas',
            name='season_reward_chest',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]