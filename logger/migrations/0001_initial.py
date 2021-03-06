# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-31 20:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Logger',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('baudrate', models.PositiveIntegerField(default=115200)),
                ('update_rate', models.PositiveIntegerField(default=0)),
                ('name', models.CharField(max_length=50)),
                ('data_port', models.CharField(default='ttyAMA0', max_length=50)),
                ('timeout', models.PositiveIntegerField(default=5)),
                ('current_time', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]

