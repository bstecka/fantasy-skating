# Generated by Django 2.1.7 on 2019-03-30 02:35

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Unknown', max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='CategoryClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='X', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='scoring.Category')),
                ('category_class', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='scoring.CategoryClass')),
            ],
        ),
        migrations.CreateModel(
            name='Competitor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=64)),
                ('start_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('end_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='Placement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_score', models.FloatField(blank=True, default=None, null=True, verbose_name='Low')),
                ('placement', models.IntegerField()),
                ('competitor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='scoring.Competitor')),
                ('event', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='scoring.Event')),
            ],
        ),
        migrations.CreateModel(
            name='Skater',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=64)),
                ('surname', models.CharField(default='', max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='UserScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='competitor',
            name='skater_1',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='skater_1', to='scoring.Skater'),
        ),
        migrations.AddField(
            model_name='competitor',
            name='skater_2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='skater_2', to='scoring.Skater'),
        ),
        migrations.AddField(
            model_name='choice',
            name='competitor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='scoring.Competitor'),
        ),
        migrations.AddField(
            model_name='choice',
            name='event',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='scoring.Event'),
        ),
        migrations.AddField(
            model_name='choice',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]