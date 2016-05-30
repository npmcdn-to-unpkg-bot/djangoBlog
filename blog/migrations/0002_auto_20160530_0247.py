# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('name', models.CharField(max_length=200, serialize=False, primary_key=True)),
            ],
        ),
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ['-modified']},
        ),
        migrations.AddField(
            model_name='article',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='blog.Tag', null=True),
        ),
    ]
