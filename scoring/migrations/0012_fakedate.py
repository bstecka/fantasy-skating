# Generated by Django 2.1.7 on 2019-07-12 22:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scoring', '0011_eventuserscore'),
    ]

    operations = [
        migrations.CreateModel(
            name='FakeDate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
            ],
        ),
    ]