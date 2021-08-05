# Generated by Django 3.2 on 2021-08-05 10:01

from django.conf import settings
import django.contrib.auth
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0002_document_stats'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.TextField()),
                ('active_models', models.JSONField(null=True)),
                ('created_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=models.SET(django.contrib.auth.get_user_model), related_name='+', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=models.SET(django.contrib.auth.get_user_model), related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
