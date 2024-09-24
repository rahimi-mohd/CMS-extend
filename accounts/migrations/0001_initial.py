# Generated by Django 5.1.1 on 2024-09-24 10:51

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_type', models.IntegerField(choices=[(1, 'Clinic Staff'), (2, 'Doctor')], default=1)),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True, unique=True)),
                ('ic_number', models.CharField(blank=True, max_length=12, null=True, unique=True)),
                ('register_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
