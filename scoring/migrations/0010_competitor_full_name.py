# Generated by Django 2.1.7 on 2019-06-26 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scoring', '0009_entry'),
    ]

    operations = [
        migrations.AddField(
            model_name='competitor',
            name='full_name',
            field=models.CharField(default='', max_length=64),
        ),
    ]