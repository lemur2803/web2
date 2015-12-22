# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-16 14:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Visit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visitor_hash', models.CharField(blank=True, db_index=True, max_length=40, null=True)),
                ('uri', models.CharField(blank=True, max_length=255, null=True)),
                ('ip_address', models.GenericIPAddressField(blank=True, db_index=True, null=True)),
                ('last_visit', models.DateTimeField(blank=True, null=True)),
                ('visits', models.IntegerField(default=0)),
                ('object_app', models.CharField(max_length=255)),
                ('object_model', models.CharField(max_length=255)),
                ('object_id', models.CharField(max_length=255)),
                ('blocked', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'visits',
                'ordering': ('uri', 'object_model', 'object_id'),
                'verbose_name': 'visit',
            },
        ),
    ]
