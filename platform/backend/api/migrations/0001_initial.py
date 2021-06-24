# Generated by Django 3.2 on 2021-06-24 14:05

import api.models
from django.conf import settings
import django.contrib.auth
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
                ('ref', models.CharField(max_length=12)),
                ('date', models.DateTimeField()),
                ('created_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=models.SET(django.contrib.auth.get_user_model), related_name='+', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=models.SET(django.contrib.auth.get_user_model), related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ExamWording',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
                ('word', models.CharField(max_length=100)),
                ('created_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=models.SET(django.contrib.auth.get_user_model), related_name='+', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=models.SET(django.contrib.auth.get_user_model), related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ExamRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
                ('ref', models.CharField(max_length=6)),
                ('created_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=models.SET(django.contrib.auth.get_user_model), related_name='+', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=models.SET(django.contrib.auth.get_user_model), related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ExamReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
                ('text', models.TextField()),
                ('features', models.JSONField()),
                ('created_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=models.SET(django.contrib.auth.get_user_model), related_name='+', to=settings.AUTH_USER_MODEL)),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.exam')),
                ('modified_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=models.SET(django.contrib.auth.get_user_model), related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='exam',
            name='room',
            field=models.ForeignKey(on_delete=models.SET(api.models.get_room_sentinel), to='api.examroom'),
        ),
        migrations.AddField(
            model_name='exam',
            name='wording',
            field=models.ForeignKey(on_delete=models.SET(api.models.get_wording_sentinel), to='api.examwording'),
        ),
    ]
