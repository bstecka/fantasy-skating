# Generated by Django 2.1.7 on 2019-06-26 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scoring', '0006_classassignmentforevent'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='short_name',
            field=models.CharField(default=models.CharField(default='', max_length=64), max_length=64),
        ),
    ]
