# Generated by Django 3.2 on 2021-05-12 12:34

import api.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ExamRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=6)),
            ],
        ),
        migrations.CreateModel(
            name='ExamWording',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=12)),
                ('date', models.DateTimeField()),
                ('added_date', models.DateField(auto_now_add=True)),
                ('modified_date', models.DateField(auto_now=True)),
                ('added_user', models.ForeignKey(on_delete=models.SET(api.models.get_sentinel_user), related_name='added_user', to=settings.AUTH_USER_MODEL)),
                ('modified_user', models.ForeignKey(on_delete=models.SET(api.models.get_sentinel_user), related_name='modified_user', to=settings.AUTH_USER_MODEL)),
                ('room_fk', models.ForeignKey(on_delete=models.SET(api.models.get_sentinel_room), to='api.examroom')),
                ('wording_fk', models.ForeignKey(on_delete=models.SET(api.models.get_sentinel_wording), to='api.examwording')),
            ],
        ),
    ]
